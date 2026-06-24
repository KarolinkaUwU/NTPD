import os
import sys
import csv

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("RDDExample") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

sc = spark.sparkContext

csv_path = "data/retail_sales_dataset.csv"

if not os.path.exists(csv_path):
    print("Nie znaleziono pliku:", csv_path)
    print("Aktualny folder:", os.getcwd())
    spark.stop()
    sys.exit()

print("=== WCZYTANIE PLIKU CSV JAKO RDD ===")

raw_rdd = sc.textFile(csv_path)

header = raw_rdd.first()
print("Nagłówek pliku:")
print(header)

data_rdd = raw_rdd.filter(lambda line: line != header)

print("\nLiczba wierszy danych bez nagłówka:")
print(data_rdd.count())


def parse_line(line):
    values = next(csv.reader([line]))

    return {
        "Transaction ID": int(values[0]),
        "Date": values[1],
        "Customer ID": values[2],
        "Gender": values[3],
        "Age": int(values[4]),
        "Product Category": values[5],
        "Quantity": int(values[6]),
        "Price per Unit": int(values[7]),
        "Total Amount": int(values[8])
    }


transactions_rdd = data_rdd.map(parse_line)

print("\n=== TRANSFORMACJA MAP ===")
print("Pierwsze 5 sparsowanych rekordów:")
for row in transactions_rdd.take(5):
    print(row)

print("\n=== TRANSFORMACJA FILTER ===")
electronics_rdd = transactions_rdd.filter(
    lambda row: row["Product Category"] == "Electronics" and row["Total Amount"] > 100
)

print("Transakcje z kategorii Electronics o wartości większej niż 100:")
for row in electronics_rdd.take(10):
    print(row)

print("\n=== AKCJA REDUCE ===")

total_sales = transactions_rdd \
    .map(lambda row: row["Total Amount"]) \
    .reduce(lambda a, b: a + b)

total_quantity = transactions_rdd \
    .map(lambda row: row["Quantity"]) \
    .reduce(lambda a, b: a + b)

print("Suma wartości sprzedaży:", total_sales)
print("Suma sprzedanych sztuk:", total_quantity)

print("\n=== GROUP BY KEY / REDUCE BY KEY ===")

sales_by_category = transactions_rdd \
    .map(lambda row: (row["Product Category"], row["Total Amount"])) \
    .reduceByKey(lambda a, b: a + b)

print("Suma sprzedaży według kategorii:")
for category, sales in sales_by_category.collect():
    print(category, ":", sales)

quantity_by_category = transactions_rdd \
    .map(lambda row: (row["Product Category"], row["Quantity"])) \
    .reduceByKey(lambda a, b: a + b)

print("\nLiczba sprzedanych sztuk według kategorii:")
for category, quantity in quantity_by_category.collect():
    print(category, ":", quantity)

print("\n=== AKCJA COLLECT ===")

category_results = sales_by_category.collect()
print("Wynik collect():")
print(category_results)

spark.stop()