import pandas as pd

ALERTS_PATH = "data/failure_alerts.csv"

df = pd.read_csv(ALERTS_PATH)

print("\nAlert Summary Report")
print("--------------------")

print(f"Total Alerts: {len(df)}")

print("\nAlerts by Severity:")
print(df["alert_severity"].value_counts())

print("\nAverage Failure Probability:")
print(round(df["failure_probability"].mean() * 100, 2), "%")

print("\nTop Risky Pipelines:")
print(
    df.groupby("pipeline_id")["failure_probability"]
    .mean()
    .sort_values(ascending=False)
    .head()
)