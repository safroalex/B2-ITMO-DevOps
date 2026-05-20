# CHANGES

## ЛР 3 — GitLab CI/CD

- Ветка `lab3`: добавлен `.gitlab-ci.yml` — стадии `test` → `build` → `deploy`, джоба `clear-job` (manual).
- `test-job`: проверка наличия непустых `lab2/dags` и `lab2/spark` на всех ветках.
- `build-job`: `docker build -t airflow-itmo:latest .`; не запускается для веток `feature/*`.
- `deploy-job`: `docker-compose up -d` только для веток `main`, `master`, `develop`.
- В `docker-compose.yml` для Airflow-сервисов задано `image: airflow-itmo:latest` вместе с `build: .` для согласованности с CI.
- Тег раннера в CI: `local-mac` (должен совпадать с тегом зарегистрированного runner).
- Пример локального runner: `lab3/gitlab-runner/docker-compose.yml`.

## ЛР 4 — Loki + Prometheus + Grafana

- Добавлены сервисы в `docker-compose.yml`: `loki`, `alloy`, `prometheus`, `grafana`
- Добавлен `alloy.conf` — сбор логов Airflow и **Spark** → Loki (`job=airflow`, `job=spark`, labels `component=master|worker`)
- Добавлен `prometheus.yml` — scrape: Prometheus, Airflow webserver, **spark-master** (`/metrics/master/prometheus/`), **spark-worker** (`/metrics/prometheus/`)
- Добавлен `lab4/spark-metrics.properties` — PrometheusServlet для master/worker (монт в `/opt/spark/conf/metrics.properties`)
- В `docker-compose.yml` для Spark: тома `./logs/spark-master`, `./logs/spark-worker`, `SPARK_*_OPTS` с `spark.ui.prometheus.enabled=true`
- Каталоги `logs/spark-master/`, `logs/spark-worker/` с `.gitkeep`

## ЛР 2 — Airflow + Spark

- Обновлён `Dockerfile`: JRE из образа `eclipse-temurin:17-jre` (без `apt-get`, стабильная сборка при недоступности deb.debian.org), `pyspark==3.5.0`, `apache-airflow-providers-apache-spark==4.1.1`
- Обновлён `docker-compose.yml`: добавлены сервисы `spark-master` и `spark-worker`
- Добавлен `lab2/dags/spark_dag.py` — DAG с `SparkSubmitOperator`
- Добавлена директория `lab2/spark/` с PySpark-джобом `stats_job.py`
- Соединение `spark_local` создаётся автоматически через `AIRFLOW_CONN_SPARK_LOCAL`

## ЛР 1 — Airflow + Docker Compose

- Создан `Dockerfile` на базе `apache/airflow:2.7.1`
- Создан `docker-compose.yml`: Airflow (webserver + scheduler + init) + PostgreSQL
- Добавлен `lab1/dags/stats_dag.py` — 4-шаговый конвейер (генерация → статистика → фильтр → отчёт)
