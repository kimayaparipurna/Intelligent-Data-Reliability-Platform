CREATE DATABASE IF NOT EXISTS reliability_platform;

USE reliability_platform;

CREATE TABLE IF NOT EXISTS pipeline_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    pipeline_id INT,
    execution_time FLOAT,
    records_processed INT,
    missing_values INT,
    duplicate_records INT,
    alert_count INT
);

CREATE TABLE IF NOT EXISTS failure_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    pipeline_id INT,
    failure_prediction INT,
    failure_probability FLOAT
);

CREATE TABLE IF NOT EXISTS failure_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    pipeline_id INT,
    failure_probability FLOAT,
    alert_severity VARCHAR(20),
    alert_message VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS model_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    training_date DATETIME,
    model_name VARCHAR(100),
    dataset_version VARCHAR(100),
    accuracy FLOAT,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT
);