"""
ЛР 2 — Airflow DAG: запуск Spark-джоба через SparkSubmitOperator
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "spark_statistics_pipeline",
    default_args=default_args,
    description="Запускает PySpark-джоб для вычисления статистики",
    schedule_interval=timedelta(days=1),
    catchup=False,
)

spark_job = SparkSubmitOperator(
    task_id="spark_statistics_job",
    application="/opt/airflow/spark/stats_job.py",
    name="statistics_spark_job",
    conn_id="spark_local",
    dag=dag,
)

spark_job
