import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, to_timestamp, lower, trim

spark = SparkSession.builder \
    .appName("LAB11_ReadStream_CSV") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

input_path = "data/input_stream"

os.makedirs(input_path, exist_ok=True)

schema = StructType([
    StructField("event_time", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("category", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("status", StringType(), True),
])

print("=== ZADANIE 2: STRUMIENIOWE WCZYTYWANIE DANYCH CSV ===")
print("Folder wejściowy strumienia:", input_path)

df_stream = spark.readStream \
    .schema(schema) \
    .option("header", True) \
    .csv(input_path)

print("\nCzy DataFrame jest strumieniowy?")
print(df_stream.isStreaming)

print("\n=== SCHEMAT POCZĄTKOWY ===")
df_stream.printSchema()

clean_df = df_stream \
    .withColumn("event_time", to_timestamp(col("event_time"))) \
    .withColumn("category", lower(trim(col("category")))) \
    .withColumn("status", lower(trim(col("status")))) \
    .filter(col("event_time").isNotNull()) \
    .filter(col("user_id").isNotNull()) \
    .filter(col("amount").isNotNull()) \
    .filter(col("amount") >= 0)

print("\n=== SCHEMAT PO CZYSZCZENIU DANYCH ===")
clean_df.printSchema()

print("\nWykonane czyszczenie danych:")
print("- konwersja event_time ze string na timestamp")
print("- usunięcie spacji oraz zamiana category i status na małe litery")
print("- odfiltrowanie rekordów bez event_time, user_id lub amount")
print("- odfiltrowanie rekordów z ujemną wartością amount")

print("\nŹródło strumieniowe zostało przygotowane poprawnie.")
print("W kolejnych zadaniach ten DataFrame będzie użyty do transformacji, agregacji i zapisu strumienia.")

spark.stop()