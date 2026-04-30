"""
ЛР 2 — PySpark job: статистика и распределение случайных чисел
Запускается через SparkSubmitOperator из spark_dag.py
"""

import random
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg, stddev, min as spark_min, max as spark_max,
    count, floor, col,
)

SPARK_MASTER = "spark://spark-master:7077"

conf = (
    SparkConf()
    .setAppName("StatisticsJob")
    .setMaster(SPARK_MASTER)
    .set("spark.executor.memory", "512m")
    .set("spark.executor.memoryOverhead", "128m")
    .set("spark.driver.memory", "512m")
    .set("spark.driver.memoryOverhead", "128m")
    .set("spark.executor.cores", "1")
)

spark = SparkSession.builder.config(conf=conf).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# ── Генерация данных ──────────────────────────────────────────────────────────
random.seed(42)
data = [(i, random.randint(1, 1000)) for i in range(1000)]
df = spark.createDataFrame(data, ["id", "value"])

# ── Общая статистика ──────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("  ОБЩАЯ СТАТИСТИКА (1000 случайных чисел от 1 до 1000)")
print("=" * 50)
df.select(
    count("value").alias("count"),
    avg("value").alias("mean"),
    stddev("value").alias("stdev"),
    spark_min("value").alias("min"),
    spark_max("value").alias("max"),
).show()

# ── Чётные / нечётные ────────────────────────────────────────────────────────
even_count = df.filter(col("value") % 2 == 0).count()
total = df.count()
print(f"  Чётных : {even_count} / {total} ({even_count / total * 100:.1f}%)")
print(f"  Нечётных: {total - even_count} / {total}\n")

# ── Распределение по сотням ───────────────────────────────────────────────────
print("=" * 50)
print("  РАСПРЕДЕЛЕНИЕ ПО ДИАПАЗОНАМ (шаг 100)")
print("=" * 50)
df.withColumn("range_start", (floor(col("value") / 100) * 100).cast("int")) \
  .groupBy("range_start") \
  .agg(count("value").alias("count")) \
  .orderBy("range_start") \
  .show()

spark.stop()
