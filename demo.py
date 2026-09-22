import os
import subprocess
import threading
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

PYTHON = os.path.join( PROJECT_DIR, ".venv", "Scripts", "python.exe")
MACHINE_SCRIPT = os.path.join( PROJECT_DIR, "simulator", "machine.py")
DASHBOARD_SCRIPT = os.path.join( PROJECT_DIR, "dashboard", "app.py")

machine_process = None
dashboard_process = None

def start_machine(fault_mode=False):

    global machine_process
    stop_machine()

    environment = os.environ.copy()
    environment["FAULT_MODE"] = ( "true" if fault_mode else "false")
    machine_process = subprocess.Popen(
        [PYTHON, MACHINE_SCRIPT],
        cwd=PROJECT_DIR,
        env=environment
    )

def stop_machine():

    global machine_process

    if machine_process is not None:
        if machine_process.poll() is None:
            machine_process.terminate()
        machine_process = None

def start_dashboard():

    global dashboard_process

    if dashboard_process is None:
        dashboard_process = subprocess.Popen(
            [
                PYTHON,
                "-m",
                "streamlit",
                "run",
                DASHBOARD_SCRIPT,
                "--server.headless",
                "true"
            ],
            cwd=PROJECT_DIR
        )

        # Give Streamlit a few seconds to start
        threading.Thread(
            target=open_dashboard,
            daemon=True
        ).start()

def open_dashboard():

    time.sleep(3)
    webbrowser.open( "http://localhost:8501")

def start_demo():

    start_dashboard()
    start_machine(fault_mode=False)

    status_label.config( text="🟢 NORMAL MODE", fg="green")

def change_mode():

    fault_mode = mode_var.get()
    start_machine( fault_mode=fault_mode)

    if fault_mode:
        status_label.config( text="🔴 FAULT MODE", fg="red")

    else:
        status_label.config( text="🟢 NORMAL MODE", fg="green")

def stop_demo():

    stop_machine()
    global dashboard_process

    if dashboard_process is not None:
        if dashboard_process.poll() is None:
            dashboard_process.terminate()
        dashboard_process = None

    status_label.config(text="⚪ DEMO STOPPED", fg="gray")

def on_close():

    stop_demo()
    root.destroy()

root = tk.Tk()

root.title("Smart Factory Demo")
root.geometry("500x400")
root.resizable(False, False)

root.protocol( "WM_DELETE_WINDOW", on_close)

title = tk.Label( root, text="🏭 Smart Factory", font=("Arial", 24, "bold"))
title.pack( pady=(30, 5))

subtitle = tk.Label( root, text="Industry 4.0 — IIoT Machine Monitoring", font=("Arial", 12))
subtitle.pack( pady=(0, 25))


start_button = tk.Button(
    root,
    text="▶ START DEMO",
    font=("Arial", 14, "bold"),
    width=20,
    height=2,
    command=start_demo
)

start_button.pack( pady=10)

mode_var = tk.BooleanVar( value=False)

fault_switch = tk.Checkbutton(
    root,
    text="Simulate Machine Fault",
    variable=mode_var,
    font=("Arial", 13, "bold"),
    command=change_mode
)

fault_switch.pack( pady=20)

status_label = tk.Label(
    root,
    text="⚪ DEMO STOPPED",
    font=("Arial", 16, "bold"),
    fg="gray"
)

status_label.pack( pady=15)

stop_button = tk.Button(
    root,
    text="■ STOP DEMO",
    font=("Arial", 12),
    width=20,
    height=2,
    command=stop_demo
)

stop_button.pack( pady=10)
root.mainloop()