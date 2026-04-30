FROM apache/airflow:2.7.1

WORKDIR /opt/airflow

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends procps default-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY ./lab1/dags/ ./dags/
COPY ./lab2/dags/ ./dags/
COPY ./lab2/spark/ ./spark/
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.1.1 \
    pyspark==3.5.0
