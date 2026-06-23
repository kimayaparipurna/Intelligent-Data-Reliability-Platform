import pandas as pd
import joblib
import time
import os
from db_connection import get_connection

MODEL_PATH = "models/failure_prediction_model.pkl"
INPUT_PATH = "data/live_pipeline_logs.csv"
OUTPUT_PATH = "data/live_predictions.csv"

model = joblib.load(MODEL_PATH)

processed_rows = 0

features = [
    "pipeline_id",
    "execution_time",
    "records_processed",
    "missing_values",
    "duplicate_records",
    "alert_count"
]

print("Live Predictor Started ✅")
print("Writing predictions to CSV and MySQL ✅")

while True:
    if not os.path.exists(INPUT_PATH):
        time.sleep(2)
        continue

    df = pd.read_csv(INPUT_PATH)

    if len(df) <= processed_rows:
        time.sleep(2)
        continue

    new_data = df.iloc[processed_rows:].copy()

    X = new_data[features]

    new_data["failure_prediction"] = model.predict(X)
    new_data["failure_probability"] = model.predict_proba(X)[:, 1]

    file_exists = os.path.exists(OUTPUT_PATH)

    new_data.to_csv(
        OUTPUT_PATH,
        mode="a",
        header=not file_exists,
        index=False
    )

    connection = get_connection()

    if connection is not None:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO failure_predictions (
            timestamp,
            pipeline_id,
            failure_prediction,
            failure_probability
        )
        VALUES (%s, %s, %s, %s)
        """

        for _, row in new_data.iterrows():
            values = (
                row["timestamp"],
                int(row["pipeline_id"]),
                int(row["failure_prediction"]),
                float(row["failure_probability"])
            )

            cursor.execute(insert_query, values)

        connection.commit()
        cursor.close()
        connection.close()

    print("New prediction generated and inserted ✅")
    print(new_data[[
        "timestamp",
        "pipeline_id",
        "failure_prediction",
        "failure_probability"
    ]])

    processed_rows = len(df)

    time.sleep(2)

