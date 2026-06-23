import subprocess
import sys
import time

scripts = [
    "src/live_pipeline_simulator.py",
    "src/live_predictor.py",
    "src/live_alert_stream.py"
]

processes = []

try:
    print("Starting Intelligent Data Reliability Platform ✅")

    for script in scripts:
        process = subprocess.Popen([sys.executable, script])
        processes.append(process)
        print(f"Started: {script}")
        time.sleep(2)

    print("\nSystem running ✅")
    print("Press CTRL + C to stop all services")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping all services...")

    for process in processes:
        process.terminate()

    print("All services stopped ✅")