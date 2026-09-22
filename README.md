# Smart Factory Monitor

This is a small software-only Industry 4.0 project.

The project simulates a factory machine and sends its sensor data using MQTT. A Streamlit dashboard receives the data and shows the machine condition in real time.

The machine has four simulated parameters:

- Temperature
- Vibration
- RPM
- Current

The dashboard also checks these values and shows a warning when they go outside the normal range.

## What is used

- Python
- Mosquitto MQTT
- MQTT
- Streamlit
- Pandas

No physical hardware is required.

## How it works

```text
Machine Simulator
       |
       | MQTT
       v
Mosquitto Broker
       |
       | MQTT
       v
Streamlit Dashboard
```

The machine simulator sends data every second.

Example:

```json
{
    "temperature": 61.42,
    "vibration": 2.06,
    "rpm": 1499,
    "current": 4.35,
    "status": "RUNNING"
}
```

## Project files

```text
smart_factory/
│
├── simulator/
│   └── machine.py
│
├── dashboard/
│   └── app.py
│
├── demo.py
├── requirements.txt
└── README.md
```

`.venv` is created locally when you set up the project, so it does not need to be included in the project files.

## Requirements

This project is made for Windows 10/11.

You need:

- Python 3.10 or newer
- Mosquitto MQTT Broker
- A web browser

VS Code is optional.

The project was developed using Windows 11 and Python 3.12.

## Installation

### 1. Install Python

Install Python from:

https://www.python.org/downloads/

During installation, make sure **Add Python to PATH** is enabled.

Check the installation:

```powershell
python --version
pip --version
```

### 2. Install Mosquitto

Download the Windows installer from:

https://mosquitto.org/download/

Install it using the normal/default options.

After installation, check that the Mosquitto service is running:

```powershell
Get-Service mosquitto
```

If it is stopped:

```powershell
Start-Service mosquitto
```

The project uses MQTT port:

```text
1883
```

### 3. Open the project

Open the `smart_factory` folder in VS Code.

Open a terminal in the project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of the terminal.

### 4. Install the Python packages

Run:

```powershell
pip install -r requirements.txt
```

That's all the installation that is needed.

## Running the project

The easiest way to run everything is:

```powershell
python demo.py
```

A small Smart Factory window will open.

Click:

```text
START DEMO
```

The machine simulator and dashboard will start automatically, and the dashboard will open in the browser.

## Normal mode

When the demo starts, the machine runs in normal mode.

Typical values are:

| Parameter | Normal range |
|---|---:|
| Temperature | 55–65 °C |
| Vibration | 1.5–3.0 mm/s |
| RPM | 1400–1500 |
| Current | 4–5 A |

The dashboard should show:

```text
MACHINE OPERATING NORMALLY
```

## Simulating a fault

The demo window has a:

```text
Simulate Machine Fault
```

switch.

Turn it on.

The machine will restart with abnormal values:

| Parameter | Fault range |
|---|---:|
| Temperature | 80–95 °C |
| Vibration | 6–9 mm/s |
| RPM | 1100–1250 |
| Current | 6–8 A |

The dashboard will detect the abnormal values and show:

```text
MACHINE ANOMALY DETECTED
```

It will also show which parameters are outside the normal range.

Turn the switch off to return to normal operation.

## Machine health

The dashboard has a simple health score.

It starts at 100%.

Every abnormal parameter reduces the score by 25 points.

```text
0 abnormal values → 100%
1 abnormal value  → 75%
2 abnormal values → 50%
3 abnormal values → 25%
4 abnormal values → 0%
```

This is only a simple project metric for demonstrating machine condition.

## MQTT

The machine publishes its data to:

```text
factory/machine1/data
```

Mosquitto runs locally on:

```text
localhost:1883
```

## Manual way to run it

You normally do not need this because `demo.py` starts everything for you.

If you want to run the parts separately:

### Start the machine

```powershell
python .\simulator\machine.py
```

### Start the dashboard

Open another terminal and run:

```powershell
streamlit run .\dashboard\app.py
```

Then open:

```text
http://localhost:8501
```

Make sure Mosquitto is running before starting them.

## What the project demonstrates

This project covers a few basic Industry 4.0 ideas:

- Industrial IoT
- Machine connectivity
- MQTT communication
- Real-time monitoring
- Sensor data visualization
- Condition monitoring
- Basic anomaly detection

The project uses simulated sensor data, so no physical machine or sensors are required.

## Demo flow

For the project presentation, the easiest demonstration is:

1. Run `python demo.py`.
2. Click **START DEMO**.
3. Show the normal sensor values.
4. Show the live graphs.
5. Show the machine health score.
6. Turn on **Simulate Machine Fault**.
7. Show the abnormal values.
8. Show the anomaly warning on the dashboard.
9. Show the health score changing.
10. Turn fault mode off and return to normal operation.

## Troubleshooting

### Mosquitto is not running

Run:

```powershell
Get-Service mosquitto
```

If it is stopped:

```powershell
Start-Service mosquitto
```

### Port 1883 is already in use

This usually means Mosquitto is already running.

Check:

```powershell
Get-Service mosquitto
```

If the service is running, do not start another Mosquitto instance.

### Dashboard does not open

Run:

```powershell
streamlit run .\dashboard\app.py
```

Then open:

```text
http://localhost:8501
```

### Dashboard shows zero values

Check that:

- Mosquitto is running.
- The machine simulator is running.
- The machine is publishing to `factory/machine1/data`.
- The dashboard is using the same MQTT topic.

## Note

This is an academic demonstration project.

The machine data is simulated and the anomaly detection uses fixed thresholds. It is not a machine-learning or predictive-maintenance system.
