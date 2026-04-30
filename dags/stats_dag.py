"""
ЛР 1 — Airflow DAG: конвейер статистики
Шаги:
  1. generate_data   — генерирует 100 случайных чисел и кладёт в XCom
  2. compute_stats   — считает среднее, медиану, std, min, max
  3. filter_outliers — отфильтровывает выбросы (> 2σ от среднего)
  4. report          — печатает итоговую сводку
"""

import random
import statistics
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "statistics_pipeline",
    default_args=default_args,
    description="Генерирует набор чисел и вычисляет статистику",
    schedule_interval=timedelta(days=1),
    catchup=False,
)


def generate_data(**context):
    seed = int(context["ds_nodash"])
    random.seed(seed)
    data = [random.randint(1, 1000) for _ in range(100)]
    context["ti"].xcom_push(key="dataset", value=data)
    print(f"[generate_data] Сгенерировано {len(data)} чисел, первые 10: {data[:10]}")


def compute_stats(**context):
    data = context["ti"].xcom_pull(key="dataset", task_ids="generate_data")
    stats = {
        "count": len(data),
        "total": sum(data),
        "mean": round(statistics.mean(data), 2),
        "median": statistics.median(data),
        "stdev": round(statistics.stdev(data), 2),
        "min": min(data),
        "max": max(data),
    }
    context["ti"].xcom_push(key="stats", value=stats)
    print(f"[compute_stats] {stats}")


def filter_outliers(**context):
    data = context["ti"].xcom_pull(key="dataset", task_ids="generate_data")
    stats = context["ti"].xcom_pull(key="stats", task_ids="compute_stats")
    mean = stats["mean"]
    stdev = stats["stdev"]
    threshold = 2 * stdev
    normal = [x for x in data if abs(x - mean) <= threshold]
    outliers = [x for x in data if abs(x - mean) > threshold]
    context["ti"].xcom_push(key="normal", value=normal)
    context["ti"].xcom_push(key="outliers", value=outliers)
    print(
        f"[filter_outliers] Норма: {len(normal)}, выбросы (>2σ): {len(outliers)} — {outliers}"
    )


def report(**context):
    stats = context["ti"].xcom_pull(key="stats", task_ids="compute_stats")
    normal = context["ti"].xcom_pull(key="normal", task_ids="filter_outliers")
    outliers = context["ti"].xcom_pull(key="outliers", task_ids="filter_outliers")
    print("=" * 40)
    print("       ИТОГОВЫЙ ОТЧЁТ")
    print("=" * 40)
    print(f"  Всего чисел    : {stats['count']}")
    print(f"  Сумма          : {stats['total']}")
    print(f"  Среднее        : {stats['mean']}")
    print(f"  Медиана        : {stats['median']}")
    print(f"  Стд. отклонение: {stats['stdev']}")
    print(f"  Мин / Макс     : {stats['min']} / {stats['max']}")
    print(f"  В норме (≤2σ)  : {len(normal)}")
    print(f"  Выбросов (>2σ) : {len(outliers)}")
    print("=" * 40)


t_generate = PythonOperator(
    task_id="generate_data",
    python_callable=generate_data,
    dag=dag,
)

t_stats = PythonOperator(
    task_id="compute_stats",
    python_callable=compute_stats,
    dag=dag,
)

t_filter = PythonOperator(
    task_id="filter_outliers",
    python_callable=filter_outliers,
    dag=dag,
)

t_report = PythonOperator(
    task_id="report",
    python_callable=report,
    dag=dag,
)

t_generate >> t_stats >> t_filter >> t_report
