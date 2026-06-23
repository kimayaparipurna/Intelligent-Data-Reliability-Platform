import pandas as pd
import random
import os

OUTPUT_PATH = "data/labeled_pipeline_logs.csv"

os.makedirs("data", exist_ok=True)

data = []

for i in range(5000):
    pipeline_id = random.randint(1, 10)

    execution_time = round(random.uniform(10, 150), 2)
    records_processed = random.randint(1000, 12000)
    missing_values = random.randint(0, 100)
    duplicate_records = random.randint(0, 80)
    alert_count = random.randint(0, 10)

    risk_score = 0

    if execution_time > 100:
        risk_score += 1
    if missing_values > 50:
        risk_score += 1
    if duplicate_records > 40:
        risk_score += 1
    if alert_count > 5:
        risk_score += 1
    if records_processed < 2500:
        risk_score += 1

    # Add noise: sometimes systems fail even when signs are not obvious
    random_noise = random.random()

    if risk_score >= 5:
        failure = 1
    elif risk_score == 4:
        failure = 1 if random_noise < 0.60 else 0
    elif risk_score == 3:
        failure = 1 if random_noise < 0.25 else 0
    elif risk_score == 2:
        failure = 1 if random_noise < 0.08 else 0
    elif risk_score == 1:
        failure = 1 if random_noise < 0.02 else 0
    else:
        failure = 0

    data.append({
        "pipeline_id": pipeline_id,
        "execution_time": execution_time,
        "records_processed": records_processed,
        "missing_values": missing_values,
        "duplicate_records": duplicate_records,
        "alert_count": alert_count,
        "failure": failure
    })

df = pd.DataFrame(data)

df.to_csv(OUTPUT_PATH, index=False)

print("Realistic labeled dataset created successfully ✅")
print(df["failure"].value_counts())
print(f"Output saved to: {OUTPUT_PATH}")