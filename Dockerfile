# JRE без apt-get (на части сетей deb.debian.org недоступен при сборке)
FROM eclipse-temurin:17-jre AS jre

FROM apache/airflow:2.7.1

WORKDIR /opt/airflow

USER root
COPY --from=jre /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER airflow
COPY ./lab1/dags/ ./dags/
COPY ./lab2/dags/ ./dags/
COPY ./lab2/spark/ ./spark/
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.1.1 \
    pyspark==3.5.0
