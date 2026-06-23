import pandas as pd
import os

INPUT_PATH = "data/predicted_pipeline_failures.csv"
OUTPUT_PATH = "data/failure_alerts.csv"

df = pd.read_csv(INPUT_PATH)

alerts = df[
    (df["failure_prediction"] == 1) |
    (df["failure_probability"] >= 0.60)
].copy()


def get_severity(prob):
    if prob >= 0.90:
        return "CRITICAL"
    elif prob >= 0.75:
        return "HIGH"
    elif prob >= 0.60:
        return "MEDIUM"
    else:
        return "LOW"


def generate_message(prob):
    if prob >= 0.90:
        return "Critical pipeline failure likely"
    elif prob >= 0.75:
        return "High pipeline failure risk detected"
    elif prob >= 0.60:
        return "Moderate pipeline failure risk detected"
    else:
        return "Low pipeline failure risk detected"


alerts["alert_severity"] = alerts["failure_probability"].apply(get_severity)
alerts["alert_message"] = alerts["failure_probability"].apply(generate_message)

os.makedirs("data", exist_ok=True)

alerts.to_csv(OUTPUT_PATH, index=False)

print("Alert Generation Complete ✅")
print(f"Total alerts generated: {len(alerts)}")
print(f"Output saved to: {OUTPUT_PATH}")

if not alerts.empty:
    print(alerts[[
        "pipeline_id",
        "failure_probability",
        "alert_severity",
        "alert_message"
    ]].head())
else:
    print("No alerts generated.")