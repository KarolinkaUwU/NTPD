import os
import sys
import csv

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, count, round as spark_round

spark = SparkSession.builder \
    .appName("DataFrameExample") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

csv_path = "data/retail_sales_dataset.csv"

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(csv_path)

print("=== WYŚWIETLANIE DANYCH ===")
df.show(10, truncate=False)

print("=== SCHEMAT DATAFRAME ===")
df.printSchema()

print("=== SELEKCJA WYBRANYCH KOLUMN ===")
selected_df = df.select(
    "Transaction ID",
    "Date",
    "Product Category",
    "Quantity",
    "Price per Unit",
    "Total Amount"
)

selected_df.show(10, truncate=False)

print("=== FILTROWANIE WIERSZY ===")
filtered_df = df.filter(
    (col("Product Category") == "Electronics") &
    (col("Total Amount") > 100)
)

filtered_df.show(10, truncate=False)

print("=== GRUPOWANIE I AGREGACJE ===")
grouped_df = df.groupBy("Product Category").agg(
    count("Transaction ID").alias("number_of_transactions"),
    spark_sum("Quantity").alias("total_quantity"),
    spark_round(spark_sum("Total Amount"), 2).alias("total_sales"),
    spark_round(avg("Price per Unit"), 2).alias("avg_price_per_unit")
)

grouped_df.show(truncate=False)

print("=== ZAPIS PRZETWORZONEGO DATAFRAME ===")

output_dir = "output"
output_file = os.path.join(output_dir, "sales_summary.csv")

os.makedirs(output_dir, exist_ok=True)

rows = grouped_df.collect()

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(grouped_df.columns)

    for row in rows:
        writer.writerow(row)

print("Przetworzony DataFrame zapisano do pliku:", output_file)

spark.stop()