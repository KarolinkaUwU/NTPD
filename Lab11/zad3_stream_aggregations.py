import os
import sys
import csv
import time
import shutil
import threading

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import (
    col,
    to_timestamp,
    lower,
    trim,
    count,
    sum as spark_sum,
    round as spark_round
)

INPUT_PATH = "data/input_stream_task3"
CHECKPOINT_PATH = "checkpoints/task3_console"


def reset_folders():
    if os.path.exists(INPUT_PATH):
        shutil.rmtree(INPUT_PATH)

    if os.path.exists(CHECKPOINT_PATH):
        shutil.rmtree(CHECKPOINT_PATH)

    os.makedirs(INPUT_PATH, exist_ok=True)
    os.makedirs(CHECKPOINT_PATH, exist_ok=True)


def write_csv_file(file_number, rows):
    file_path = os.path.join(INPUT_PATH, f"events_{file_number:03d}.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["event_time", "user_id", "category", "amount", "status"])
        writer.writerows(rows)

    print(f"[GENERATOR] Dodano plik: {file_path}")


def data_generator():
    batches = [
        [
            ["2026-05-01 10:00:00", "u001", "books", 39.99, "paid"],
            ["2026-05-01 10:01:00", "u002", "electronics", 149.90, "paid"],
            ["2026-05-01 10:02:00", "u003", "books", 25.50, "cancelled"],
        ],
        [
            ["2026-05-01 10:03:00", "u004", "clothes", 89.99, "paid"],
            ["2026-05-01 10:04:00", "u005", "electronics", 299.00, "pending"],
            ["2026-05-01 10:05:00", "u006", "books", 59.99, "paid"],
        ],
        [
            ["2026-05-01 10:06:00", "u007", "electronics", 499.00, "paid"],
            ["2026-05-01 10:07:00", "u008", "clothes", 120.00, "paid"],
            ["2026-05-01 10:08:00", "u009", "books", 19.99, "paid"],
        ],
    ]

    time.sleep(5)

    for i, rows in enumerate(batches, start=1):
        write_csv_file(i, rows)
        time.sleep(8)


reset_folders()

spark = SparkSession.builder \
    .appName("LAB11_Stream_Transformations_Aggregations") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("event_time", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("category", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("status", StringType(), True),
])

print("=== ZADANIE 3: TRANSFORMACJE I AGREGACJE STRUMIENIOWE ===")
print("Folder wejściowy:", INPUT_PATH)

df_stream = spark.readStream \
    .schema(schema) \
    .option("header", True) \
    .csv(INPUT_PATH)

clean_df = df_stream \
    .withColumn("event_time", to_timestamp(col("event_time"))) \
    .withColumn("category", lower(trim(col("category")))) \
    .withColumn("status", lower(trim(col("status")))) \
    .filter(col("event_time").isNotNull()) \
    .filter(col("amount").isNotNull()) \
    .filter(col("amount") >= 0)

paid_df = clean_df \
    .filter(col("status") == "paid") \
    .select("event_time", "user_id", "category", "amount", "status") \
    .withColumn("amount_with_tax", spark_round(col("amount") * 1.23, 2))

summary = paid_df.groupBy("category").agg(
    count("*").alias("events_count"),
    spark_round(spark_sum("amount"), 2).alias("total_amount"),
    spark_round(spark_sum("amount_with_tax"), 2).alias("total_amount_with_tax")
)

print("Czy DataFrame jest strumieniowy?")
print(summary.isStreaming)

print("\nWykonane transformacje:")
print("- konwersja event_time do typu timestamp")
print("- czyszczenie category oraz status")
print("- filtrowanie tylko statusu paid")
print("- wybór wybranych kolumn")
print("- obliczenie dodatkowej kolumny amount_with_tax")
print("- agregacja według category")

generator_thread = threading.Thread(target=data_generator)
generator_thread.daemon = True
generator_thread.start()

query = summary.writeStream \
    .format("console") \
    .outputMode("complete") \
    .option("truncate", False) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .trigger(processingTime="5 seconds") \
    .start()

query.awaitTermination(70)

if query.isActive:
    query.stop()

spark.stop()

print("Aplikacja streamingowa zakończyła działanie po czasie testowym.")