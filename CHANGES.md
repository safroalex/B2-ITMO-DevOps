# CHANGES

## ЛР 4 — Loki + Prometheus + Grafana

- Добавлены сервисы в `docker-compose.yml`: `loki`, `alloy`, `prometheus`, `grafana`
- Добавлен `alloy.conf` — конфиг сборщика логов Airflow → Loki
- Добавлен `prometheus.yml` — конфиг скрейпинга метрик Airflow

## ЛР 2 — Airflow + Spark

- Обновлён `Dockerfile`: добавлены `procps`, `default-jre`, `pyspark==3.5.0`, `apache-airflow-providers-apache-spark==4.1.1`
- Обновлён `docker-compose.yml`: добавлены сервисы `spark-master` и `spark-worker`
- Добавлен `dags/spark_dag.py` — DAG с `SparkSubmitOperator`
- Добавлена директория `spark/` с PySpark-джобом `stats_job.py`
- Соединение `spark_local` создаётся автоматически через `AIRFLOW_CONN_SPARK_LOCAL`

## ЛР 1 — Airflow + Docker Compose

- Создан `Dockerfile` на базе `apache/airflow:2.7.1`
- Создан `docker-compose.yml`: Airflow (webserver + scheduler + init) + PostgreSQL
- Добавлен `dags/stats_dag.py` — 4-шаговый конвейер (генерация → статистика → фильтр → отчёт)
