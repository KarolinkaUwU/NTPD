import os
import sys

# Wymuszenie użycia tego samego interpretera Python dla drivera i workerów PySpark
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSQL_Parquet_Read") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

parquet_path = "data/sales_data.parquet"

if not os.path.exists(parquet_path):
    print("Nie znaleziono pliku Parquet:", parquet_path)
    print("Najpierw uruchom main.py, aby przygotować plik Parquet.")
    spark.stop()
    sys.exit()

print("=== WCZYTANIE PLIKU PARQUET DO DATAFRAME ===")

df = spark.read.parquet(parquet_path)

print("Plik Parquet został poprawnie wczytany do DataFrame.")
print("Ścieżka pliku:", parquet_path)

print("\n=== PIERWSZE WIERSZE DATAFRAME ===")
df.show(10, truncate=False)

print("\n=== SCHEMAT DATAFRAME ===")
df.printSchema()

spark.stop()