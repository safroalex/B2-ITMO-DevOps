# Airflow + Spark + Loki + Prometheus + Grafana

Учебный стек для лабораторных работ 1, 2, 4 курса DevOps ИТМО.

## Состав стека

| Сервис            | URL                       | Описание                        |
|-------------------|---------------------------|---------------------------------|
| Airflow Webserver | http://localhost:8080     | login: `airflow` / `airflow`    |
| Spark Master UI   | http://localhost:4040     | Мониторинг Spark-кластера       |
| Prometheus        | http://localhost:9090     | Метрики Airflow                 |
| Grafana           | http://localhost:3000     | Дашборды (анонимный доступ)     |
| Loki              | http://localhost:3100     | Хранилище логов (internal)      |

## DAG-и

| DAG                         | Файл                  | Описание                                                                       |
|-----------------------------|-----------------------|--------------------------------------------------------------------------------|
| `statistics_pipeline`       | `dags/stats_dag.py`   | ЛР 1 — генерация → статистика → фильтр выбросов → отчёт (4 Python-оператора) |
| `spark_statistics_pipeline` | `dags/spark_dag.py`   | ЛР 2 — SparkSubmitOperator запускает `spark/stats_job.py`                     |

## Деплой локально

```bash
mkdir -p logs && chmod 777 logs
docker compose up -d
# дождаться ~2 мин, затем открыть http://localhost:8080
# login: airflow / airflow
```

## Деплой на сервер

```bash
git clone <repo-url> /opt/airflow-lab
cd /opt/airflow-lab
mkdir -p logs && chmod 777 logs
docker compose up -d
```

## Настройка Grafana (ЛР 4)

1. Открыть http://\<server\>:3000
2. Connections → Data sources → Add → **Loki** → URL: `http://loki:3100` → Save & Test
3. Connections → Data sources → Add → **Prometheus** → URL: `http://prometheus:9090` → Save & Test
4. Explore → Loki → Label: `job = airflow_logs` → Run query
5. Add to dashboard → создать дашборд с двумя плитками (логи + метрика из Prometheus)

> **Примечание:** подключение к Spark (`spark_local`) создаётся **автоматически** через `AIRFLOW_CONN_SPARK_LOCAL` — вручную создавать в Admin UI ничего не нужно.