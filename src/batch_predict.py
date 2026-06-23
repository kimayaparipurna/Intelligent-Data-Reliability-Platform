import pandas as pd
import joblib
import os

MODEL_PATH = "models/failure_prediction_model.pkl"
DATA_PATH = "data/labeled_pipeline_logs.csv"
OUTPUT_PATH = "data/predicted_pipeline_failures.csv"

model = joblib.load(MODEL_PATH)

df = pd.read_csv(DATA_PATH)

features = [
    "pipeline_id",
    "execution_time",
    "records_processed",
    "missing_values",
    "duplicate_records",
    "alert_count"
]

X = df[features]

df["failure_prediction"] = model.predict(X)
df["failure_probability"] = model.predict_proba(X)[:, 1]

os.makedirs("data", exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print("Batch Prediction Complete ✅")
print(f"Output saved to: {OUTPUT_PATH}")
print(df[["failure", "failure_prediction", "failure_probability"]].head())