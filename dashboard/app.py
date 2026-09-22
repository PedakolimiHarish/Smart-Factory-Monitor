import json
import time
import threading
from collections import deque

import paho.mqtt.client as mqtt
import streamlit as st
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/machine1/data"

MAX_HISTORY = 60


# -----------------------------
# Shared machine data
# -----------------------------

if "machine_data" not in st.session_state:

    st.session_state.machine_data = {
        "temperature": 0.0,
        "vibration": 0.0,
        "rpm": 0.0,
        "current": 0.0,
        "status": "WAITING"
    }


if "history" not in st.session_state:

    st.session_state.history = {
        "temperature": deque(maxlen=MAX_HISTORY),
        "vibration": deque(maxlen=MAX_HISTORY),
        "rpm": deque(maxlen=MAX_HISTORY),
        "current": deque(maxlen=MAX_HISTORY)
    }


if "mqtt_started" not in st.session_state:
    st.session_state.mqtt_started = False


# -----------------------------
# MQTT callback
# -----------------------------

def on_message(client, userdata, message):

    try:

        data = json.loads(message.payload.decode())

        lock = userdata["lock"]

        with lock:

            userdata["data"].update(data)

            userdata["history"]["temperature"].append(
                data["temperature"]
            )

            userdata["history"]["vibration"].append(
                data["vibration"]
            )

            userdata["history"]["rpm"].append(
                data["rpm"]
            )

            userdata["history"]["current"].append(
                data["current"]
            )

    except Exception as e:

        print(f"MQTT error: {e}")


# -----------------------------
# Start MQTT
# -----------------------------

if not st.session_state.mqtt_started:

    data_lock = threading.Lock()

    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    mqtt_client.user_data_set({
        "data": st.session_state.machine_data,
        "history": st.session_state.history,
        "lock": data_lock
    })

    mqtt_client.on_message = on_message

    mqtt_client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    mqtt_client.subscribe(MQTT_TOPIC)

    mqtt_client.loop_start()

    st.session_state.mqtt_client = mqtt_client
    st.session_state.data_lock = data_lock
    st.session_state.mqtt_started = True


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Smart Factory Monitor",
    page_icon="🏭",
    layout="wide"
)


# -----------------------------
# Read current data
# -----------------------------

with st.session_state.data_lock:

    data = st.session_state.machine_data.copy()

    history = {
        key: list(values)
        for key, values in st.session_state.history.items()
    }


# -----------------------------
# Dashboard
# -----------------------------

st.title("🏭 Smart Factory Monitor")

st.caption(
    "Industry 4.0 — Industrial IoT Machine Monitoring"
)


# -----------------------------
# Condition monitoring
# -----------------------------

temperature_fault = data["temperature"] > 75
vibration_fault = data["vibration"] > 5
rpm_fault = data["rpm"] < 1300
current_fault = data["current"] > 6


anomaly_detected = (
    temperature_fault
    or vibration_fault
    or rpm_fault
    or current_fault
)


# -----------------------------
# Machine status
# -----------------------------

if anomaly_detected:

    st.error("🔴 MACHINE ANOMALY DETECTED")

else:

    st.success("🟢 MACHINE OPERATING NORMALLY")


# -----------------------------
# Detected problems
# -----------------------------

if anomaly_detected:

    st.subheader("⚠️ Detected Problems")

    if temperature_fault:

        st.warning(
            f"High temperature: "
            f"{data['temperature']:.2f} °C"
        )

    if vibration_fault:

        st.warning(
            f"High vibration: "
            f"{data['vibration']:.2f} mm/s"
        )

    if rpm_fault:

        st.warning(
            f"Low RPM: "
            f"{data['rpm']:.0f} RPM"
        )

    if current_fault:

        st.warning(
            f"High current: "
            f"{data['current']:.2f} A"
        )

# -----------------------------
# Machine health score
# -----------------------------

health_score = 100


if temperature_fault:
    health_score -= 25

if vibration_fault:
    health_score -= 25

if rpm_fault:
    health_score -= 25

if current_fault:
    health_score -= 25


health_score = max(0, health_score)

# -----------------------------
# Machine health
# -----------------------------

st.subheader("Machine Health")

st.progress(
    health_score / 100
)

st.metric(
    "Health Score",
    f"{health_score}%"
)

# -----------------------------
# Current sensor values
# -----------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Temperature",
        f"{data['temperature']:.2f} °C"
    )


with col2:

    st.metric(
        "Vibration",
        f"{data['vibration']:.2f} mm/s"
    )


with col3:

    st.metric(
        "RPM",
        f"{data['rpm']:.0f}"
    )


with col4:

    st.metric(
        "Current",
        f"{data['current']:.2f} A"
    )


# -----------------------------
# Machine information
# -----------------------------

st.divider()

st.subheader("Machine Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.write("**Machine ID:** machine1")

with info2:
    st.write("**Communication:** MQTT")

with info3:
    st.write("**Broker:** localhost:1883")


# -----------------------------
# Historical data
# -----------------------------

st.divider()

st.subheader("📈 Machine Data History")


if len(history["temperature"]) > 0:

    df = pd.DataFrame(history)

    # -----------------------------
    # Temperature
    # -----------------------------

    st.write("### 🌡️ Motor Temperature")

    st.line_chart(
        df["temperature"],
        height=250
    )

    st.caption("Temperature (°C)")


    # -----------------------------
    # Vibration
    # -----------------------------

    st.write("### 📳 Motor Vibration")

    st.line_chart(
        df["vibration"],
        height=250
    )

    st.caption("Vibration (mm/s)")


    # -----------------------------
    # RPM
    # -----------------------------

    st.write("### ⚙️ Motor Speed")

    st.line_chart(
        df["rpm"],
        height=250
    )

    st.caption("Speed (RPM)")


    # -----------------------------
    # Current
    # -----------------------------

    st.write("### ⚡ Motor Current")

    st.line_chart(
        df["current"],
        height=250
    )

    st.caption("Current (A)")


else:

    st.info("Waiting for machine data...")

# -----------------------------
# Auto refresh
# -----------------------------

time.sleep(1)

st.rerun()