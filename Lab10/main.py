import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSQL_Parquet") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Apache Spark jest zainstalowany i skonfigurowany poprawnie.")
print("Nazwa aplikacji:", spark.sparkContext.appName)
print("Wersja Spark:", spark.version)
print("Tryb pracy:", spark.sparkContext.master)
print("Interpreter Python:", sys.executable)

os.makedirs("data", exist_ok=True)

parquet_path = "data/sales_data.parquet"

data = {
    "transaction_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "date": [
        "2024-01-05", "2024-01-07", "2024-01-10", "2024-01-12",
        "2024-02-01", "2024-02-03", "2024-02-05", "2024-02-07"
    ],
    "city": [
        "Bydgoszcz", "Warszawa", "Krakow", "Gdansk",
        "Bydgoszcz", "Warszawa", "Krakow", "Gdansk"
    ],
    "product_category": [
        "Electronics", "Clothing", "Beauty", "Electronics",
        "Clothing", "Beauty", "Electronics", "Clothing"
    ],
    "quantity": [2, 1, 3, 1, 4, 2, 1, 5],
    "unit_price": [1500, 250, 80, 3200, 120, 60, 2100, 90],
    "total_amount": [3000, 250, 240, 3200, 480, 120, 2100, 450]
}

df_pandas = pd.DataFrame(data)
df_pandas.to_parquet(parquet_path, index=False)

print("Plik Parquet został przygotowany:")
print(parquet_path)

spark.stop()