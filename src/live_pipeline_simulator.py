import pandas as pd
import random
import time
import os
from datetime import datetime
from db_connection import get_connection

OUTPUT_PATH = "data/live_pipeline_logs.csv"

os.makedirs("data", exist_ok=True)

columns = [
    "timestamp",
    "pipeline_id",
    "execution_time",
    "records_processed",
    "missing_values",
    "duplicate_records",
    "alert_count"
]

if not os.path.exists(OUTPUT_PATH):
    pd.DataFrame(columns=columns).to_csv(OUTPUT_PATH, index=False)

print("Live Pipeline Simulator Started ✅")
print("Writing logs to CSV and MySQL ✅")
print("Press CTRL + C to stop")

while True:
    pipeline_id = random.randint(1, 10)
    execution_time = round(random.uniform(10, 120), 2)
    records_processed = random.randint(1000, 10000)
    missing_values = random.randint(0, 80)
    duplicate_records = random.randint(0, 60)
    alert_count = random.randint(0, 8)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_log = pd.DataFrame([{
        "timestamp": timestamp,
        "pipeline_id": pipeline_id,
        "execution_time": execution_time,
        "records_processed": records_processed,
        "missing_values": missing_values,
        "duplicate_records": duplicate_records,
        "alert_count": alert_count
    }])

    new_log.to_csv(OUTPUT_PATH, mode="a", header=False, index=False)

    connection = get_connection()

    if connection is not None:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO pipeline_logs (
            timestamp,
            pipeline_id,
            execution_time,
            records_processed,
            missing_values,
            duplicate_records,
            alert_count
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            timestamp,
            pipeline_id,
            execution_time,
            records_processed,
            missing_values,
            duplicate_records,
            alert_count
        )

        cursor.execute(insert_query, values)
        connection.commit()

        cursor.close()
        connection.close()

    print("New live log generated and inserted ✅")
    print(new_log)

    time.sleep(1)