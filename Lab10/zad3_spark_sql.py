import os
import sys
import csv

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSQL_Queries") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

sales_csv_path = "data/retail_sales_dataset.csv"
category_csv_path = "data/product_categories.csv"

if not os.path.exists(sales_csv_path):
    print("Nie znaleziono pliku:", sales_csv_path)
    spark.stop()
    sys.exit()

os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Przygotowanie drugiego pliku CSV do wykonania JOIN
with open(category_csv_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["product_category", "department", "margin_level"])
    writer.writerow(["Beauty", "Personal Care", "Medium"])
    writer.writerow(["Clothing", "Fashion", "High"])
    writer.writerow(["Electronics", "Technology", "Low"])

print("=== WCZYTANIE DANYCH DO DATAFRAME ===")

df_sales = spark.read.csv(
    sales_csv_path,
    header=True,
    inferSchema=True
)

df_categories = spark.read.csv(
    category_csv_path,
    header=True,
    inferSchema=True
)

print("Dane sprzedażowe:")
df_sales.show(5, truncate=False)

print("Dane kategorii:")
df_categories.show(truncate=False)

print("=== REJESTRACJA WIDOKÓW TYMCZASOWYCH ===")

df_sales.createOrReplaceTempView("retail_sales")
df_categories.createOrReplaceTempView("product_categories")

print("Zarejestrowano widoki: retail_sales oraz product_categories")

print("\n=== 1. AGREGACJE: SUM, AVG, COUNT ===")

aggregation_result = spark.sql("""
    SELECT
        COUNT(*) AS number_of_transactions,
        SUM(`Total Amount`) AS total_sales,
        AVG(`Total Amount`) AS avg_transaction_value,
        SUM(`Quantity`) AS total_quantity
    FROM retail_sales
""")

aggregation_result.show(truncate=False)

print("\n=== 2. GRUPOWANIE PO KATEGORII PRODUKTU ===")

group_by_category_result = spark.sql("""
    SELECT
        `Product Category` AS product_category,
        COUNT(*) AS number_of_transactions,
        SUM(`Quantity`) AS total_quantity,
        SUM(`Total Amount`) AS total_sales,
        ROUND(AVG(`Total Amount`), 2) AS avg_transaction_value
    FROM retail_sales
    GROUP BY `Product Category`
    ORDER BY total_sales DESC
""")

group_by_category_result.show(truncate=False)

print("\n=== 3. GRUPOWANIE PO KATEGORII I PŁCI ===")

group_by_category_gender_result = spark.sql("""
    SELECT
        `Product Category` AS product_category,
        Gender,
        COUNT(*) AS number_of_transactions,
        SUM(`Total Amount`) AS total_sales
    FROM retail_sales
    GROUP BY `Product Category`, Gender
    ORDER BY product_category, Gender
""")

group_by_category_gender_result.show(truncate=False)

print("\n=== 4. WARUNKOWE FILTROWANIE: TRANSAKCJE POWYŻEJ 1000 ===")

filtered_result = spark.sql("""
    SELECT
        `Transaction ID`,
        Date,
        `Customer ID`,
        Gender,
        Age,
        `Product Category`,
        Quantity,
        `Price per Unit`,
        `Total Amount`
    FROM retail_sales
    WHERE `Total Amount` > 1000
    ORDER BY `Total Amount` DESC
    LIMIT 10
""")

filtered_result.show(truncate=False)

print("\n=== 5. JOIN DWÓCH WIDOKÓW ===")

join_result = spark.sql("""
    SELECT
        r.`Product Category` AS product_category,
        c.department,
        c.margin_level,
        COUNT(*) AS number_of_transactions,
        SUM(r.`Quantity`) AS total_quantity,
        SUM(r.`Total Amount`) AS total_sales,
        ROUND(AVG(r.`Total Amount`), 2) AS avg_transaction_value
    FROM retail_sales r
    JOIN product_categories c
        ON r.`Product Category` = c.product_category
    GROUP BY
        r.`Product Category`,
        c.department,
        c.margin_level
    ORDER BY total_sales DESC
""")

join_result.show(truncate=False)

print("\n=== ZAPIS WYNIKU ZAPYTANIA SQL DO CSV ===")

output_file = "output/spark_sql_join_summary.csv"

rows = join_result.collect()

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(join_result.columns)

    for row in rows:
        writer.writerow(row)

print("Wynik zapytania SQL zapisano do pliku:", output_file)

spark.stop()