import pandas as pd
import time
import os
from db_connection import get_connection

INPUT_PATH = "data/live_predictions.csv"
OUTPUT_PATH = "data/live_alerts.csv"

processed_rows = 0

print("Live Alert Stream Started ✅")
print("Writing alerts to CSV and MySQL ✅")


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


while True:
    if not os.path.exists(INPUT_PATH):
        time.sleep(2)
        continue

    df = pd.read_csv(INPUT_PATH)

    if len(df) <= processed_rows:
        time.sleep(2)
        continue

    new_data = df.iloc[processed_rows:].copy()

    alerts = new_data[
        (new_data["failure_prediction"] == 1) |
        (new_data["failure_probability"] >= 0.60)
    ].copy()

    if not alerts.empty:
        alerts["alert_severity"] = alerts["failure_probability"].apply(get_severity)
        alerts["alert_message"] = alerts["failure_probability"].apply(generate_message)

        file_exists = os.path.exists(OUTPUT_PATH)

        alerts.to_csv(
            OUTPUT_PATH,
            mode="a",
            header=not file_exists,
            index=False
        )

        connection = get_connection()

        if connection is not None:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO failure_alerts (
                timestamp,
                pipeline_id,
                failure_probability,
                alert_severity,
                alert_message
            )
            VALUES (%s, %s, %s, %s, %s)
            """

            for _, row in alerts.iterrows():
                values = (
                    row["timestamp"],
                    int(row["pipeline_id"]),
                    float(row["failure_probability"]),
                    row["alert_severity"],
                    row["alert_message"]
                )

                cursor.execute(insert_query, values)

            connection.commit()
            cursor.close()
            connection.close()

        print("New live alert generated and inserted 🚨")
        print(alerts[[
            "timestamp",
            "pipeline_id",
            "failure_probability",
            "alert_severity",
            "alert_message"
        ]])

    processed_rows = len(df)

    time.sleep(2)