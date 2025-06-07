import streamlit as st
import json
import os
from datetime import datetime
import uuid
import pandas as pd
import requests

st.set_page_config(page_title="MES Dashboard", layout="wide")

DATA_DIR = "data"
ORDERS_FILE = os.path.join(DATA_DIR, "work_orders.json")
STATUS_FILE = os.path.join(DATA_DIR, "machine_status.json")
API_BASE_URL = "http://localhost:5001"

# Utility functions
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Auto-refresh every 15 seconds
st_autorefresh_interval = 15000  # ms
st.markdown(
    f"""
    <meta http-equiv="refresh" content="{st_autorefresh_interval / 1000}">
    """,
    unsafe_allow_html=True
)

st.title("?? MES + IoT Dashboard")

# 1. ?? Work Order Submission Form
st.subheader("?? Submit New Work Order")
with st.form("work_order_form"):
    product = st.text_input("Product Name", value="WidgetA")
    quantity = st.number_input("Quantity", min_value=1, value=100)
    machine_id = st.text_input("Target Machine ID", value="M001")
    submitted = st.form_submit_button("Submit Work Order")

    if submitted:
        orders = load_json(ORDERS_FILE)
        new_order = {
            "order_id": f"WO_{uuid.uuid4().hex[:6].upper()}",
            "product": product,
            "quantity": quantity,
            "machine_id": machine_id,
            "status": "PENDING"
        }
        orders.append(new_order)
        save_json(ORDERS_FILE, orders)
        st.success(f"? Order submitted: {new_order['order_id']}")

# 2. ?? View Work Orders with Send Button
st.subheader("?? All Work Orders")
orders = load_json(ORDERS_FILE)

if orders:
    for order in orders:
        cols = st.columns([3, 2, 2, 2, 2])
        cols[0].markdown(f"**{order['order_id']}**")
        cols[1].markdown(f"{order['product']}")
        cols[2].markdown(f"{order['quantity']}")
        cols[3].markdown(f"{order['status']}")
        if order['status'] == "PENDING":
            if cols[4].button("?? Send", key=order['order_id']):
                url = f"{API_BASE_URL}/api/work-orders/{order['order_id']}/send"
                try:
                    response = requests.post(url)
                    if response.status_code == 200:
                        st.success(f"? Sent order {order['order_id']}")
                    else:
                        st.error(f"? Failed: {response.json().get('error')}")
                except Exception as e:
                    st.error(f"?? Connection Error: {e}")
else:
    st.info("No work orders available.")

# 3. ?? Machine Status Updates
st.subheader("?? Machine Status Updates")
status_logs = load_json(STATUS_FILE)
if status_logs:
    st.json(status_logs[-5:])
else:
    st.info("No machine status yet.")

# 4. ?? Charts: Machine Load (from Status Log)
st.subheader("?? Machine Metrics")
if status_logs:
    df = pd.DataFrame(status_logs)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.line_chart(df.groupby("machine_id").size())
else:
    st.warning("Not enough data for metrics yet.")
