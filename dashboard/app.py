import sys
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from db_connection import get_connection


st.set_page_config(
    page_title="Intelligent Data Reliability Platform",
    layout="wide"
)

st_autorefresh(interval=5000, key="dashboard_refresh")

st.title("🚀 Intelligent Data Reliability Platform")
st.caption("Live ML-powered pipeline reliability monitoring dashboard")


def load_table(table_name):
    connection = get_connection()

    if connection is None:
        return pd.DataFrame()

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)

    connection.close()
    return df


pipeline_logs = load_table("pipeline_logs")
predictions = load_table("failure_predictions")
alerts = load_table("failure_alerts")
metrics = load_table("model_metrics")


if not pipeline_logs.empty:
    pipeline_logs["timestamp"] = pd.to_datetime(pipeline_logs["timestamp"])

if not predictions.empty:
    predictions["timestamp"] = pd.to_datetime(predictions["timestamp"])

if not alerts.empty:
    alerts["timestamp"] = pd.to_datetime(alerts["timestamp"])

if not metrics.empty:
    metrics["training_date"] = pd.to_datetime(metrics["training_date"])


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Overview",
    "Alert Command Center",
    "Pipeline Health",
    "Model Monitoring",
    "Live Operations"
])


# =========================
# PAGE 1: EXECUTIVE OVERVIEW
# =========================
with tab1:
    st.subheader("Executive Overview")

    total_logs = len(pipeline_logs)
    total_predictions = len(predictions)
    total_alerts = len(alerts)

    failure_rate = 0
    if total_predictions > 0:
        failure_rate = round(
            (predictions["failure_prediction"].sum() / total_predictions) * 100,
            2
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Pipeline Logs", total_logs)
    col2.metric("Total Predictions", total_predictions)
    col3.metric("Total Alerts", total_alerts)
    col4.metric("Failure Rate", f"{failure_rate}%")

    st.divider()

    if not pipeline_logs.empty:
        execution_trend = pipeline_logs.sort_values("timestamp").tail(100)

        fig = px.line(
            execution_trend,
            x="timestamp",
            y="execution_time",
            title="Execution Time Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

    if not predictions.empty:
        probability_trend = predictions.sort_values("timestamp").tail(100)

        fig = px.line(
            probability_trend,
            x="timestamp",
            y="failure_probability",
            title="Failure Probability Trend"
        )

        st.plotly_chart(fig, use_container_width=True)


# =========================
# PAGE 2: ALERT COMMAND CENTER
# =========================
with tab2:
    st.subheader("Alert Command Center 🚨")

    if alerts.empty:
        st.info("No alerts found.")
    else:
        critical_count = len(alerts[alerts["alert_severity"] == "CRITICAL"])
        high_count = len(alerts[alerts["alert_severity"] == "HIGH"])
        medium_count = len(alerts[alerts["alert_severity"] == "MEDIUM"])
        low_count = len(alerts[alerts["alert_severity"] == "LOW"])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Critical Alerts", critical_count)
        col2.metric("High Alerts", high_count)
        col3.metric("Medium Alerts", medium_count)
        col4.metric("Low Alerts", low_count)

        st.divider()

        severity_counts = alerts["alert_severity"].value_counts().reset_index()
        severity_counts.columns = ["severity", "count"]

        fig = px.pie(
            severity_counts,
            names="severity",
            values="count",
            title="Alert Severity Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        alert_trend = (
            alerts.sort_values("timestamp")
            .tail(100)
            .groupby(alerts["timestamp"].dt.strftime("%H:%M:%S"))
            .size()
            .reset_index(name="alert_count")
        )

        fig = px.line(
            alert_trend,
            x="timestamp",
            y="alert_count",
            title="Alert Volume Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

        top_alerting = alerts["pipeline_id"].value_counts().reset_index()
        top_alerting.columns = ["pipeline_id", "alert_count"]

        fig = px.bar(
            top_alerting,
            x="pipeline_id",
            y="alert_count",
            title="Top Alerting Pipelines"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Latest Alerts")
        st.dataframe(
            alerts.sort_values("id", ascending=False).head(50),
            use_container_width=True
        )

        st.subheader("Critical Alerts Only")
        st.dataframe(
            alerts[alerts["alert_severity"] == "CRITICAL"]
            .sort_values("id", ascending=False)
            .head(50),
            use_container_width=True
        )


# =========================
# PAGE 3: PIPELINE HEALTH
# =========================
with tab3:
    st.subheader("Pipeline Health 🔍")

    if predictions.empty:
        st.info("No prediction data found.")
    else:
        pipeline_risk = (
            predictions.groupby("pipeline_id")
            .agg(
                avg_failure_probability=("failure_probability", "mean"),
                max_failure_probability=("failure_probability", "max"),
                total_predictions=("id", "count"),
                predicted_failures=("failure_prediction", "sum")
            )
            .reset_index()
            .sort_values("avg_failure_probability", ascending=False)
        )

        fig = px.bar(
            pipeline_risk,
            x="pipeline_id",
            y="avg_failure_probability",
            title="Average Failure Probability by Pipeline"
        )

        st.plotly_chart(fig, use_container_width=True)

        if not pipeline_logs.empty:
            execution_by_pipeline = (
                pipeline_logs.groupby("pipeline_id")["execution_time"]
                .mean()
                .reset_index()
                .sort_values("execution_time", ascending=False)
            )

            fig = px.bar(
                execution_by_pipeline,
                x="pipeline_id",
                y="execution_time",
                title="Average Execution Time by Pipeline"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Pipeline Risk Ranking")
        st.dataframe(
            pipeline_risk,
            use_container_width=True
        )

        st.subheader("Recent Predictions")
        st.dataframe(
            predictions.sort_values("id", ascending=False).head(50),
            use_container_width=True
        )


# =========================
# PAGE 4: MODEL MONITORING
# =========================
with tab4:
    st.subheader("ML Model Monitoring 🤖")

    if metrics.empty:
        st.info("No model metrics found.")
    else:
        latest = metrics.sort_values("id", ascending=False).iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Accuracy", round(latest["accuracy"], 4))
        col2.metric("Precision", round(latest["precision_score"], 4))
        col3.metric("Recall", round(latest["recall_score"], 4))
        col4.metric("F1 Score", round(latest["f1_score"], 4))

        st.divider()

        metrics_sorted = metrics.sort_values("training_date")

        fig = px.line(
            metrics_sorted,
            x="training_date",
            y=[
                "accuracy",
                "precision_score",
                "recall_score",
                "f1_score"
            ],
            title="Model Metrics Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Training History")
        st.dataframe(
            metrics.sort_values("id", ascending=False),
            use_container_width=True
        )


# =========================
# PAGE 5: LIVE OPERATIONS
# =========================
with tab5:
    st.subheader("Live Operations ⚡")

    col1, col2, col3 = st.columns(3)

    col1.metric("Live Logs", len(pipeline_logs))
    col2.metric("Live Predictions", len(predictions))
    col3.metric("Live Alerts", len(alerts))

    st.divider()

    st.subheader("Latest Live Logs")
    if not pipeline_logs.empty:
        st.dataframe(
            pipeline_logs.sort_values("id", ascending=False).head(25),
            use_container_width=True
        )

    st.subheader("Latest Live Predictions")
    if not predictions.empty:
        st.dataframe(
            predictions.sort_values("id", ascending=False).head(25),
            use_container_width=True
        )

    st.subheader("Latest Live Alerts")
    if not alerts.empty:
        st.dataframe(
            alerts.sort_values("id", ascending=False).head(25),
            use_container_width=True
        )