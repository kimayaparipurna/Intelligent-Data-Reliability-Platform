import pandas as pd
import joblib


model = joblib.load("models/failure_prediction_model.pkl")


sample_run = pd.DataFrame([
    {
        "pipeline_id": 3,
        "execution_time": 4.2,
        "records_processed": 3500,
        "missing_values": 1,
        "duplicate_records": 0,
        "alert_count": 0
    }
])

prediction = model.predict(sample_run)[0]
probability = model.predict_proba(sample_run)[0][1]

if prediction == 1:
    print("Prediction: Failure Risk Detected")
else:
    print("Prediction: Pipeline Healthy")

print(f"Failure Probability: {probability:.2%}")