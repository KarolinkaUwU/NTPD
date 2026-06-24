import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = "data/transactions.csv"

engine = create_engine("postgresql+psycopg2://bi:bi@127.0.0.1:5433/ntpd")

df = pd.read_csv(CSV_PATH)

df["event_time"] = pd.to_datetime(df["event_time"])
df["amount"] = df["amount"].astype(float)

df.to_sql("transactions", engine, if_exists="replace", index=False)

print("Załadowano dane do tabeli transactions.")
print("Liczba wierszy:", len(df))
print("Kolumny:", list(df.columns))
print(df.head())