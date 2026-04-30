# B2-ITMO-DevOps — Лабораторные работы

Репозиторий содержит лабораторные работы 1, 2, 4 по курсу DevOps (ИТМО).  
Все сервисы поднимаются единым `docker compose up -d` из корня репозитория.

## Структура репозитория

```
.
├── Dockerfile                  # Кастомный образ Airflow с Java и PySpark
├── docker-compose.yml          # Все сервисы: Airflow, Spark, Loki, Prometheus, Grafana
├── .env.example                # Шаблон переменных окружения → скопировать в .env
│
├── lab1/
│   ├── dags/stats_dag.py       # ЛР 1: Python-пайплайн статистики (4 задачи, XCom)
│   └── screenshots/            # Скриншоты выполнения
│
├── lab2/
│   ├── dags/spark_dag.py       # ЛР 2: DAG с SparkSubmitOperator
│   ├── spark/stats_job.py      # PySpark-джоб вычисления статистики
│   └── screenshots/            # Скриншоты выполнения + Spark Master UI
│
├── lab3/                       # ЛР 3: CI/CD (выполняется отдельно)
│
└── lab4/
    ├── alloy.conf              # Grafana Alloy: сбор логов Airflow → Loki
    ├── prometheus.yml          # Prometheus: scrape-конфиг
    └── screenshots/            # Скриншоты Grafana, Prometheus
```

## Требования

- Docker Desktop ≥ 24 (или Docker Engine + Docker Compose v2)
- 4 GB RAM (минимум), рекомендуется 6 GB
- Свободные порты: 8080, 4040, 7077, 9090, 3000, 3100

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/safroalex/B2-ITMO-DevOps.git
cd B2-ITMO-DevOps

# 2. Создать .env (Linux — автоматически, macOS — вручную)
# Linux:
echo "AIRFLOW_UID=$(id -u)" > .env
# macOS:
cp .env.example .env           # AIRFLOW_UID=50000 подходит для macOS

# 3. Создать директорию для логов
mkdir -p logs && chmod 777 logs

# 4. Поднять стек
docker compose up -d

# 5. Дождаться готовности (~2 минуты)
docker compose ps              # все сервисы должны быть healthy/running
```

## Адреса сервисов

| Сервис          | URL                        | Credentials           |
|-----------------|----------------------------|-----------------------|
| Airflow         | http://localhost:8080      | `airflow` / `airflow` |
| Spark Master UI | http://localhost:4040      | —                     |
| Prometheus      | http://localhost:9090      | —                     |
| Grafana         | http://localhost:3000      | `admin` / `admin`     |
| Loki            | http://localhost:3100      | (internal)            |

## ЛР 1 — Airflow Python Pipeline

**DAG:** `statistics_pipeline` → [lab1/dags/stats_dag.py](lab1/dags/stats_dag.py)

Пайплайн из 4 шагов (PythonOperator + XCom):
1. `generate_data` — генерирует 100 случайных чисел
2. `compute_stats` — среднее, медиана, std, min, max
3. `filter_outliers` — фильтрует выбросы (> 2σ)
4. `report` — итоговая сводка в логи

**Запуск:**
1. Открыть http://localhost:8080, войти `airflow / airflow`
2. Найти DAG `statistics_pipeline`, снять паузу (toggle слева)
3. Нажать ▶ (Trigger DAG)
4. Дождаться зелёных квадратиков (все 4 задачи — success)

## ЛР 2 — Airflow + Apache Spark

**DAG:** `spark_statistics_pipeline` → [lab2/dags/spark_dag.py](lab2/dags/spark_dag.py)  
**Spark job:** [lab2/spark/stats_job.py](lab2/spark/stats_job.py)

Запускает PySpark-джоб через `SparkSubmitOperator`. Кластер: 1 воркер, 2 GB памяти.  
Подключение к Spark (`spark_local`) создаётся **автоматически** через переменную окружения `AIRFLOW_CONN_SPARK_LOCAL` — вручную в UI создавать ничего не нужно.

**Запуск:**
1. Открыть http://localhost:8080
2. Найти DAG `spark_statistics_pipeline`, снять паузу
3. Нажать ▶ (Trigger DAG)
4. Задача `spark_statistics_job` выполняется ~8 секунд → success
5. Spark Master UI: http://localhost:4040 — видны воркер и история запусков

## ЛР 4 — Мониторинг: Loki + Prometheus + Grafana

Конфигурации: [lab4/alloy.conf](lab4/alloy.conf), [lab4/prometheus.yml](lab4/prometheus.yml)

Grafana Alloy читает логи из `logs/**/*.log` и пушит в Loki.  
Prometheus скрейпит себя (метрика `up` по job `prometheus`).

### Первичная настройка Grafana

1. Открыть http://localhost:3000, войти `admin / admin`
2. **Connections → Data sources → Add data source → Loki**
   - URL: `http://loki:3100`
   - Нажать **Save & Test** → должно быть "Data source connected"
3. **Connections → Data sources → Add data source → Prometheus**
   - URL: `http://prometheus:9090`
   - Нажать **Save & Test** → должно быть "Data source is working"
4. **Dashboards → New → New dashboard → Add visualization**
   - Панель 1 (Logs): тип **Logs**, источник Loki, запрос `{job="airflow"}`
   - Панель 2 (Metrics): тип **Time series**, источник Prometheus, запрос `up`

### Проверка данных

```bash
# Проверить что Loki получает логи (должны появиться labels после запуска DAG)
curl http://localhost:3100/loki/api/v1/labels

# Проверить Prometheus targets (prometheus — UP, airflow — DOWN без statsd)
curl http://localhost:9090/api/v1/targets | python3 -m json.tool
```

## Остановка стека

```bash
docker compose down         # остановить контейнеры (данные сохраняются)
docker compose down -v      # + удалить volumes (сброс базы Airflow)
```

## Troubleshooting

| Проблема | Решение |
|----------|---------|
| `Permission denied` в логах Airflow | `chmod 777 logs/` |
| Порт 7000 занят (macOS) | Маппинг `7001:7000` уже настроен в docker-compose.yml |
| Spark "no resources accepted" | `SPARK_WORKER_MEMORY=2g` задан в docker-compose.yml |
| Alloy не читает логи | Запустите DAG — логи появятся, Alloy подхватит автоматически |
| Airflow инициализируется долго | Подождите 2–3 минуты после `docker compose up -d` |
