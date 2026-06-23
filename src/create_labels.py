import pandas as pd


df = pd.read_csv("data/pipeline_logs.csv")

df["failure"] = 0

df.loc[
    (
        (df["execution_time"] > 10) &
        (df["missing_values"] > 7)
    ) |
    (
        (df["duplicate_records"] > 3) &
        (df["alert_count"] > 1)
    ) |
    (
        (df["records_processed"] < 600)
    ),
    "failure"
] = 1

df.to_csv("data/labeled_pipeline_logs.csv", index=False)

print("Labeled dataset created successfully!")
print(df["failure"].value_counts())