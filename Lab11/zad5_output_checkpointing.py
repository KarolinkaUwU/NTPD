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
    round as spark_round
)

INPUT_PATH = "data/input_stream_task5"
OUTPUT_PATH = "data/output_stream_task5"
FILE_CHECKPOINT = "checkpoints/task5_file_sink"
CONSOLE_CHECKPOINT = "checkpoints/task5_console_sink"


def reset_for_first_run():
    for path in [INPUT_PATH, OUTPUT_PATH, FILE_CHECKPOINT, CONSOLE_CHECKPOINT]:
        if os.path.exists(path):
            shutil.rmtree(path)

    os.makedirs(INPUT_PATH, exist_ok=True)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    os.makedirs(FILE_CHECKPOINT, exist_ok=True)
    os.makedirs(CONSOLE_CHECKPOINT, exist_ok=True)


def prepare_for_second_run():
    os.makedirs(INPUT_PATH, exist_ok=True)
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    os.makedirs(FILE_CHECKPOINT, exist_ok=True)
    os.makedirs(CONSOLE_CHECKPOINT, exist_ok=True)


def write_csv_file(file_name, rows):
    file_path = os.path.join(INPUT_PATH, file_name)

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["event_time", "user_id", "category", "amount", "status"])
        writer.writerows(rows)

    print(f"[GENERATOR] Dodano plik: {file_path}")


def data_generator(mode):
    time.sleep(5)

    if mode == "first":
        batches = [
            (
                "events_001.csv",
                [
                    ["2026-05-01 10:00:00", "u001", "books", 39.99, "paid"],
                    ["2026-05-01 10:01:00", "u002", "electronics", 149.90, "paid"],
                    ["2026-05-01 10:02:00", "u003", "books", 25.50, "cancelled"],
                ]
            ),
            (
                "events_002.csv",
                [
                    ["2026-05-01 10:03:00", "u004", "clothes", 89.99, "paid"],
                    ["2026-05-01 10:04:00", "u005", "electronics", 299.00, "pending"],
                    ["2026-05-01 10:05:00", "u006", "books", 59.99, "paid"],
                ]
            )
        ]

    elif mode == "second":
        timestamp = int(time.time())

        batches = [
            (
                f"events_003_new_{timestamp}.csv",
                [
                    ["2026-05-01 10:06:00", "u007", "electronics", 499.00, "paid"],
                    ["2026-05-01 10:07:00", "u008", "clothes", 120.00, "paid"],
                    ["2026-05-01 10:08:00", "u009", "books", 19.99, "cancelled"],
                ]
            )
        ]

    else:
        print("Nieznany tryb. Użyj: first albo second.")
        return

    for file_name, rows in batches:
        write_csv_file(file_name, rows)
        time.sleep(6)


mode = sys.argv[1] if len(sys.argv) > 1 else "first"

if mode == "first":
    print("=== TRYB FIRST: czyszczenie folderów wejścia, wyjścia i checkpointów ===")
    reset_for_first_run()
elif mode == "second":
    print("=== TRYB SECOND: checkpointy zostają zachowane ===")
    prepare_for_second_run()
else:
    print("Użycie:")
    print("python zad5_output_checkpointing.py first")
    print("python zad5_output_checkpointing.py second")
    sys.exit()

spark = SparkSession.builder \
    .appName("LAB11_Output_Checkpointing") \
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

print("\n=== ZADANIE 5: ZAPIS WYNIKÓW I CHECKPOINTING ===")
print("Folder wejściowy:", INPUT_PATH)
print("Folder wynikowy:", OUTPUT_PATH)
print("Checkpoint dla zapisu do plików:", FILE_CHECKPOINT)
print("Checkpoint dla konsoli:", CONSOLE_CHECKPOINT)

df_stream = spark.readStream \
    .schema(schema) \
    .option("header", True) \
    .option("maxFilesPerTrigger", 1) \
    .csv(INPUT_PATH)

processed_df = df_stream \
    .withColumn("event_time", to_timestamp(col("event_time"))) \
    .withColumn("category", lower(trim(col("category")))) \
    .withColumn("status", lower(trim(col("status")))) \
    .filter(col("event_time").isNotNull()) \
    .filter(col("amount").isNotNull()) \
    .filter(col("amount") >= 0) \
    .filter(col("status") == "paid") \
    .select("event_time", "user_id", "category", "amount", "status") \
    .withColumn("amount_with_tax", spark_round(col("amount") * 1.23, 2))

print("\nCzy DataFrame jest strumieniowy?")
print(processed_df.isStreaming)

print("\nWykonane przetwarzanie:")
print("- odczyt plików CSV jako strumień")
print("- konwersja event_time do timestamp")
print("- czyszczenie category i status")
print("- filtrowanie tylko statusu paid")
print("- obliczenie amount_with_tax")
print("- zapis wyniku do CSV")
print("- zapis stanu przetwarzania w checkpointach")

file_query = processed_df.writeStream \
    .format("csv") \
    .outputMode("append") \
    .option("path", OUTPUT_PATH) \
    .option("checkpointLocation", FILE_CHECKPOINT) \
    .option("header", True) \
    .trigger(processingTime="5 seconds") \
    .start()

console_query = processed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .option("checkpointLocation", CONSOLE_CHECKPOINT) \
    .trigger(processingTime="5 seconds") \
    .start()

generator_thread = threading.Thread(target=data_generator, args=(mode,))
generator_thread.daemon = True
generator_thread.start()

generator_thread.join()

time.sleep(15)

file_query.processAllAvailable()
console_query.processAllAvailable()

if file_query.isActive:
    file_query.stop()

if console_query.isActive:
    console_query.stop()

print("\n=== WCZYTANIE ZAPISANYCH WYNIKÓW JAKO DATAFRAME BATCH ===")

try:
    batch_df = spark.read.csv(
        OUTPUT_PATH,
        header=True,
        inferSchema=True
    )

    print("Zapisane wyniki z folderu output_stream_task5:")
    batch_df.show(truncate=False)

    print("Liczba rekordów w zapisanych wynikach:", batch_df.count())

    print("\nSchemat zapisanych danych:")
    batch_df.printSchema()

except Exception as e:
    print("Nie udało się wczytać zapisanych wyników.")
    print(e)

spark.stop()

print("\nAplikacja zakończyła działanie.")