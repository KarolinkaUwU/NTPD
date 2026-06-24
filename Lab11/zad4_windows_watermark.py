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
    window,
    count,
    sum as spark_sum,
    round as spark_round
)

INPUT_PATH = "data/input_stream_task4"
CHECKPOINT_TUMBLING = "checkpoints/task4_tumbling"
CHECKPOINT_SLIDING = "checkpoints/task4_sliding"


def reset_folders():
    if os.path.exists(INPUT_PATH):
        shutil.rmtree(INPUT_PATH)

    if os.path.exists(CHECKPOINT_TUMBLING):
        shutil.rmtree(CHECKPOINT_TUMBLING)

    if os.path.exists(CHECKPOINT_SLIDING):
        shutil.rmtree(CHECKPOINT_SLIDING)

    os.makedirs(INPUT_PATH, exist_ok=True)
    os.makedirs(CHECKPOINT_TUMBLING, exist_ok=True)
    os.makedirs(CHECKPOINT_SLIDING, exist_ok=True)


def write_csv_file(file_name, rows):
    file_path = os.path.join(INPUT_PATH, file_name)

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["event_time", "user_id", "category", "amount", "status"])
        writer.writerows(rows)

    print(f"[GENERATOR] Dodano plik: {file_path}")


def data_generator():
    batches = [
        (
            "events_001_ordered.csv",
            [
                ["2026-05-01 10:00:00", "u001", "books", 39.99, "paid"],
                ["2026-05-01 10:02:00", "u002", "electronics", 149.90, "paid"],
                ["2026-05-01 10:04:00", "u003", "books", 25.50, "paid"],
            ]
        ),
        (
            "events_002_ordered.csv",
            [
                ["2026-05-01 10:11:00", "u004", "clothes", 89.99, "paid"],
                ["2026-05-01 10:14:00", "u005", "books", 59.99, "paid"],
                ["2026-05-01 10:16:00", "u006", "electronics", 299.00, "paid"],
            ]
        ),
        (
            "events_003_watermark_advance.csv",
            [
                ["2026-05-01 10:35:00", "u007", "books", 70.00, "paid"],
                ["2026-05-01 10:36:00", "u008", "clothes", 110.00, "paid"],
            ]
        ),
        (
            "events_004_late.csv",
            [
                ["2026-05-01 10:05:00", "u009", "books", 999.00, "paid"],
                ["2026-05-01 10:07:00", "u010", "electronics", 777.00, "paid"],
            ]
        ),
        (
            "events_005_new.csv",
            [
                ["2026-05-01 10:42:00", "u011", "electronics", 500.00, "paid"],
                ["2026-05-01 10:44:00", "u012", "books", 35.00, "paid"],
            ]
        ),
    ]

    time.sleep(5)

    for file_name, rows in batches:
        write_csv_file(file_name, rows)
        time.sleep(8)


reset_folders()

spark = SparkSession.builder \
    .appName("LAB11_Windows_Watermarking") \
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

print("=== ZADANIE 4: OKNA CZASOWE I WATERMARKING ===")
print("Folder wejściowy:", INPUT_PATH)
print("Watermark: 10 minut")
print("Okna stałe: 10 minut")
print("Okna przesuwające: 10 minut, przesunięcie co 5 minut")

df_stream = spark.readStream \
    .schema(schema) \
    .option("header", True) \
    .option("maxFilesPerTrigger", 1) \
    .csv(INPUT_PATH)

clean_df = df_stream \
    .withColumn("event_time", to_timestamp(col("event_time"))) \
    .withColumn("category", lower(trim(col("category")))) \
    .withColumn("status", lower(trim(col("status")))) \
    .filter(col("event_time").isNotNull()) \
    .filter(col("amount").isNotNull()) \
    .filter(col("amount") >= 0) \
    .filter(col("status") == "paid")

print("Czy DataFrame jest strumieniowy?")
print(clean_df.isStreaming)

print("\nDane testowe obejmują:")
print("- zdarzenia w poprawnej kolejności")
print("- zdarzenia opóźnione")
print("- różne kategorie: books, electronics, clothes")
print("- różne wartości amount")

tumbling_summary = clean_df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "10 minutes"),
        col("category")
    ) \
    .agg(
        count("*").alias("events_count"),
        spark_round(spark_sum("amount"), 2).alias("total_amount")
    ) \
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("category"),
        col("events_count"),
        col("total_amount")
    ) \
    .orderBy("window_start", "category")

sliding_summary = clean_df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "10 minutes", "5 minutes"),
        col("category")
    ) \
    .agg(
        count("*").alias("events_count"),
        spark_round(spark_sum("amount"), 2).alias("total_amount")
    ) \
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("category"),
        col("events_count"),
        col("total_amount")
    ) \
    .orderBy("window_start", "category")

generator_thread = threading.Thread(target=data_generator)
generator_thread.daemon = True
generator_thread.start()

tumbling_query = tumbling_summary.writeStream \
    .queryName("tumbling_windows") \
    .format("console") \
    .outputMode("complete") \
    .option("truncate", False) \
    .option("checkpointLocation", CHECKPOINT_TUMBLING) \
    .trigger(processingTime="5 seconds") \
    .start()

sliding_query = sliding_summary.writeStream \
    .queryName("sliding_windows") \
    .format("console") \
    .outputMode("complete") \
    .option("truncate", False) \
    .option("checkpointLocation", CHECKPOINT_SLIDING) \
    .trigger(processingTime="5 seconds") \
    .start()

generator_thread.join()

time.sleep(25)

if tumbling_query.isActive:
    tumbling_query.processAllAvailable()
    tumbling_query.stop()

if sliding_query.isActive:
    sliding_query.processAllAvailable()
    sliding_query.stop()

spark.stop()

print("Aplikacja z oknami czasowymi i watermarkingiem zakończyła działanie.")