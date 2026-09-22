import os
import random
import time
import json

import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MACHINE_ID = "machine1"
MQTT_TOPIC = f"factory/{MACHINE_ID}/data"

FAULT_MODE = os.getenv("FAULT_MODE", "false").lower() == "true"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.connect( MQTT_BROKER, MQTT_PORT, 60)

# ----------------------------- 
# Debug information
# -----------------------------
""" print("Connected to MQTT broker")
print(f"Machine ID: {MACHINE_ID}")

if FAULT_MODE:
    print("⚠️ FAULT MODE ENABLED")
else:
    print("🟢 NORMAL MODE")

print()
 """

def generate_machine_data():

    if FAULT_MODE:

        # Abnormal machine condition
        temperature = random.uniform(80, 95)
        vibration = random.uniform(6, 9)
        rpm = random.uniform(1100, 1250)
        current = random.uniform(6, 8)
        status = "FAULT"

    else:

        # Normal machine condition
        temperature = random.uniform(55, 65)
        vibration = random.uniform(1.5, 3.0)
        rpm = random.uniform(1400, 1500)
        current = random.uniform(4.0, 5.0)
        status = "RUNNING"

    return {
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 2),
        "rpm": round(rpm, 2),
        "current": round(current, 2),
        "status": status
    }

while True:

    data = generate_machine_data()
    client.publish( MQTT_TOPIC, json.dumps(data))

    """ print(
        f"Temperature: {data['temperature']} °C | "
        f"Vibration: {data['vibration']} mm/s | "
        f"RPM: {data['rpm']:.0f} | "
        f"Current: {data['current']} A | "
        f"Status: {data['status']}"
    ) """

    time.sleep(1)