import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSQL_CSV") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

csv_path = "data/retail_sales_dataset.csv"

if not os.path.exists(csv_path):
    print("Nie znaleziono pliku CSV:", csv_path)
    print("Sprawdź nazwę pliku w folderze data.")
    spark.stop()
    sys.exit()

print("=== WCZYTANIE PLIKU CSV DO DATAFRAME ===")

df_csv = spark.read.csv(
    csv_path,
    header=True,
    inferSchema=True
)

print("Plik CSV został poprawnie wczytany do DataFrame.")
print("Ścieżka pliku:", csv_path)
print("Liczba wierszy:", df_csv.count())
print("Kolumny:", df_csv.columns)

print("\n=== PODGLĄD DANYCH CSV ===")
df_csv.show(10, truncate=False)

print("\n=== SCHEMAT DANYCH CSV ===")
df_csv.printSchema()

print("\n=== REJESTRACJA DATAFRAME JAKO WIDOK TYMCZASOWY ===")

df_csv.createOrReplaceTempView("retail_sales")

print("DataFrame został zarejestrowany jako widok tymczasowy: retail_sales")

print("\n=== PROSTE ZAPYTANIE SQL ===")

sql_result = spark.sql("""
    SELECT *
    FROM retail_sales
    LIMIT 10
""")

sql_result.show(truncate=False)

spark.stop()