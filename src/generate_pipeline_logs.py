import pandas as pd
import numpy as np

np.random.seed(42)

num_records = 5000

data = {
    "pipeline_id": np.random.randint(1, 11, num_records),
    "execution_time": np.random.normal(5, 2, num_records),
    "records_processed": np.random.randint(500, 5000, num_records),
    "missing_values": np.random.randint(0, 10, num_records),
    "duplicate_records": np.random.randint(0, 5, num_records),
    "alert_count": np.random.randint(0, 3, num_records)
}

df = pd.DataFrame(data)

df.to_csv("data/pipeline_logs.csv", index=False)

print("Pipeline Logs Generated Successfully!")
print(df.head())