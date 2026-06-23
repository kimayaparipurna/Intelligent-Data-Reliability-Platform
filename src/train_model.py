import pandas as pd
import joblib
import os
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from db_connection import get_connection

DATA_PATH = "data/labeled_pipeline_logs.csv"
MODEL_PATH = "models/failure_prediction_model.pkl"

os.makedirs("models", exist_ok=True)

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
y = df["failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

y_prob = model.predict_proba(X_test)[:, 1]
y_pred = (y_prob >= 0.25).astype(int)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

joblib.dump(model, MODEL_PATH)

print(f"Model Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print("Model Saved Successfully!")

connection = get_connection()

if connection is not None:
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO model_metrics (
        training_date,
        model_name,
        dataset_version,
        accuracy,
        precision_score,
        recall_score,
        f1_score
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "RandomForestClassifier",
        "realistic_v1",
        float(accuracy),
        float(precision),
        float(recall),
        float(f1)
    )

    cursor.execute(insert_query, values)
    connection.commit()

    cursor.close()
    connection.close()

    print("Model metrics saved to MySQL ✅")
else:
    print("Model trained, but metrics were not saved to MySQL ❌")