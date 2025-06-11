from flask import Flask, request, jsonify
import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from threading import Thread

app = Flask(__name__)

WORK_ORDER_FILE = "data/work_orders.json"
MACHINE_STATUS_FILE = "data/machine_status.json"
MQTT_BROKER = "localhost"  # Or use IP like "192.168.137.14"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Load existing JSON from file
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

# Save JSON to file
def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --------------------------------------------------------
# REST ENDPOINTS
# --------------------------------------------------------

@app.route('/api/work-orders', methods=['GET'])
def get_work_orders():
    """
    Returns the list of all work orders as JSON.
    """
    return jsonify(load_json(WORK_ORDER_FILE))

@app.route('/api/machine-status', methods=['POST'])
def post_machine_status():
    """
    Accepts a machine status update (JSON) and appends it to machine_status.json.
    """
    status = request.json
    statuses = load_json(MACHINE_STATUS_FILE)
    statuses.append(status)
    save_json(MACHINE_STATUS_FILE, statuses)
    return jsonify({"message": "Status received"})

@app.route('/api/work-orders/<order_id>/send', methods=['POST'])
def send_work_order(order_id):
    """
    Publishes a work order (identified by order_id) to the MQTT topic
    so that the corresponding ESP32 can pick it up.
    """
    orders = load_json(WORK_ORDER_FILE)
    for order in orders:
        if order["order_id"] == order_id:
            topic = f"work-orders/{order['machine_id']}"
            payload = json.dumps(order)
            publish.single(topic, payload, hostname=MQTT_BROKER)
            return jsonify({"message": f"Order {order_id} sent to {topic}"})
    return jsonify({"error": "Order not found"}), 404

# --------------------------------------------------------
# MQTT HANDLER
# --------------------------------------------------------

def on_mqtt_message(client, userdata, msg):
    """
    Callback whenever a machine ACK arrives on topic 'machine/ack/+'.
    Parses the ACK payload and updates the corresponding work_order's status.
    """
    try:
        ack = json.loads(msg.payload.decode())
        print(f"[MQTT] Received ACK: {ack}")
        orders = load_json(WORK_ORDER_FILE)
        for order in orders:
            if order["order_id"] == ack["order_id"]:
                order["status"] = ack["status"]
                break
        save_json(WORK_ORDER_FILE, orders)
        print(f"[MQTT] Order {ack['order_id']} updated to {ack['status']}")
    except Exception as e:
        print(f"[MQTT] Error processing message: {e}")

def mqtt_thread():
    """
    Starts a long-running MQTT client that subscribes to 'machine/ack/+' and
    invokes on_mqtt_message whenever an ACK arrives.
    """
    client = mqtt.Client()
    client.on_message = on_mqtt_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe("machine/ack/+")
    client.loop_forever()

# --------------------------------------------------------
# ENTRY POINT
# --------------------------------------------------------
@app.route('/')
def index():
    return "MES Server is Running. Use /api/* endpoints."

if __name__ == "__main__":
    # Run MQTT listener in the background
    Thread(target=mqtt_thread, daemon=True).start()

    # Read the HTTP port from environment variable (default to 5000)
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask dev server on port {port} (MQTT thread running in background)")
    app.run(host="0.0.0.0", port=port)
