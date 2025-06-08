MES Server with MQTT and Dashboard

Lightweight MES (Manufacturing Execution System) Server running on Raspberry Pi
Edge → ESP32 → MQTT → MES Server → Dashboard


🚀 Project Summary
This project implements a lightweight Manufacturing Execution System (MES) that:

✅ Sends work orders to ESP32-based machines via MQTT
✅ Receives machine acknowledgments and updates order status
✅ Stores work orders and machine statuses in JSON files
✅ Provides REST API to manage and send work orders
✅ Provides Streamlit dashboard for monitoring the MES in real time
✅ Runs behind NGINX reverse proxy (optional)
✅ Supports HTTPS with Let's Encrypt (optional)
✅ Ready to integrate with Azure Cloud IoT Hub

Architecture:
          +------------------------+
          |   MES Server (Flask)   |
          |   REST API + MQTT      |
          +-----------+------------+
                      |
                      v
                +-----------+
                | Mosquitto |
                |  MQTT Broker |
                +-----------+
                      |
                      v
        +-------------------------+
        |      ESP32 Devices      |
        |  - Subscribe to topics  |
        |  - Send ACK messages    |
        +-------------------------+

 +--------------------+
 | Streamlit Dashboard|
 | Real-time Status   |
 +--------------------+

 +------------------+       (Future)
 | Azure IoT Hub    |
 | Cloud Integration|
 +------------------+

Components
Raspberry Pi running Ubuntu / Raspberry Pi OS

Mosquitto MQTT Broker

Flask + Gunicorn app (MES REST API)

Streamlit dashboard (visual monitoring)

Supervisor for auto-start on boot

NGINX (reverse proxy and optional HTTPS)

Git for version control

ESP32 devices running MQTT firmware


📜 Features
REST API for:

Viewing work orders

Sending work orders to specific machines

Receiving machine status updates

MQTT Integration:

Publish work orders to work-orders/{machine_id}

Subscribe to machine/ack/+ for acknowledgments

Real-time Dashboard:

List of work orders and statuses

Live machine updates

Auto-start with Supervisor

Reverse proxy with NGINX

Future: Integration with Azure IoT Hub


 Running the Project
1️⃣ Clone the repo
bash

git clone https://github.com/arefin7/MES_server.git
cd MES_server
2️⃣ Setup Python virtual environment
bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3️⃣ Run Flask API
bash

export PORT=5001  # or 5000
python app.py
Or using Gunicorn:

bash

gunicorn -b 0.0.0.0:5001 app:app -c gunicorn_config.py
4️⃣ Run Streamlit Dashboard
bash

python dashboard.py
# or
streamlit run dashboard.py
5️⃣ Supervisor (auto-start)
bash

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mes
6️⃣ NGINX + HTTPS (optional)
Reverse proxy https://your-public-ip/ → local :5001

Secured with Let's Encrypt

🏭 Current Status
✅ Working locally
✅ ESP32 devices connected
✅ MQTT flow functional
✅ Dashboard working
✅ Git version controlled
✅ Supervisor running
✅ NGINX reverse proxy tested
🚧 Next: Azure Cloud IoT integration

🌐 Future Roadmap
 Add Azure IoT Hub integration

 Add Database (SQLite/Postgres) instead of JSON files

 Add authentication to REST API

 Add role-based dashboard (operator, manager view)

 Dockerize the application for easy deployment

 Continuous deployment pipeline

📚 Learning Outcome
✅ Real-world Edge → MQTT → Cloud architecture
✅ Git-based version control and CI ready
✅ Use of Supervisor, NGINX, Gunicorn for production-grade deployment
✅ Streamlit for visualization
✅ Secure deployment with HTTPS
✅ Ready for Cloud IoT integration (Azure)

💻 Developed By
Nazmul Arefin
Industrial IoT Architect | Edge Developer
