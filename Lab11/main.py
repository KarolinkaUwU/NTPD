import os
import sys

# Wymuszenie użycia tego samego interpretera Python dla drivera i workerów PySpark
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
import pyspark

spark = SparkSession.builder \
    .appName("LAB11_StructuredStreaming") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("Apache Spark oraz PySpark działają poprawnie.")
print("Nazwa aplikacji:", spark.sparkContext.appName)
print("Wersja Spark:", spark.version)
print("Wersja PySpark:", pyspark.__version__)
print("Tryb pracy:", spark.sparkContext.master)
print("Interpreter Python:", sys.executable)

spark.stop()