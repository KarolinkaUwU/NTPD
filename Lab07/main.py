import pandas as pd
from sklearn.datasets import make_classification


# 1. Generowanie zbioru historycznego
# Dane historyczne reprezentują dane z okresu trenowania/walidacji modelu.
X_train, y_train = make_classification(
    n_samples=500,
    n_features=5,
    n_informative=4,
    n_redundant=1,
    random_state=42
)

df_train = pd.DataFrame(
    X_train,
    columns=[f"feature_{i}" for i in range(5)]
)

df_train["target"] = y_train


# 2. Generowanie zbioru produkcyjnego
# Dane produkcyjne reprezentują nowsze próbki, które pojawiły się po wdrożeniu modelu.
X_prod, y_prod = make_classification(
    n_samples=300,
    n_features=5,
    n_informative=4,
    n_redundant=1,
    random_state=999
)

df_prod = pd.DataFrame(
    X_prod,
    columns=[f"feature_{i}" for i in range(5)]
)

df_prod["target"] = y_prod


# 3. Podgląd danych
print("Dane historyczne:")
print(df_train.head())

print("\nDane produkcyjne:")
print(df_prod.head())

from sklearn.ensemble import RandomForestClassifier


# 4. Trenowanie modelu ML na danych historycznych
model = RandomForestClassifier(random_state=42)

model.fit(
    df_train.drop("target", axis=1),
    df_train["target"]
)


# 5. Uzyskanie predykcji dla danych produkcyjnych
df_prod["prediction"] = model.predict(
    df_prod.drop("target", axis=1)
)


# 6. Podgląd danych produkcyjnych z predykcjami
print("\nDane produkcyjne z predykcjami:")
print(df_prod.head())

import os

# 7. Zapis danych do plików CSV
os.makedirs("data", exist_ok=True)

df_train.to_csv("data/train_data.csv", index=False)
df_prod.to_csv("data/production_data_with_predictions.csv", index=False)

print("\nDane zostały zapisane do folderu data:")
print("data/train_data.csv")
print("data/production_data_with_predictions.csv")

# 8. Wczytanie zapisanych danych z plików CSV
df_train_loaded = pd.read_csv("data/train_data.csv")
df_prod_loaded = pd.read_csv("data/production_data_with_predictions.csv")


# 9. Wstępna analiza danych historycznych
print("\n=== ANALIZA DANYCH HISTORYCZNYCH ===")
print("Liczba rekordów i kolumn:")
print(df_train_loaded.shape)

print("\nTypy zmiennych:")
print(df_train_loaded.dtypes)

print("\nLiczba braków danych:")
print(df_train_loaded.isnull().sum())

print("\nRozkład klas target:")
print(df_train_loaded["target"].value_counts())


# 10. Wstępna analiza danych produkcyjnych
print("\n=== ANALIZA DANYCH PRODUKCYJNYCH ===")
print("Liczba rekordów i kolumn:")
print(df_prod_loaded.shape)

print("\nTypy zmiennych:")
print(df_prod_loaded.dtypes)

print("\nLiczba braków danych:")
print(df_prod_loaded.isnull().sum())

print("\nRozkład klas target:")
print(df_prod_loaded["target"].value_counts())

print("\nRozkład predykcji modelu:")
print(df_prod_loaded["prediction"].value_counts())


# 11. Podstawowe statystyki opisowe
print("\nStatystyki opisowe danych historycznych:")
print(df_train_loaded.describe())

print("\nStatystyki opisowe danych produkcyjnych:")
print(df_prod_loaded.describe())

import os

from evidently import Report
from evidently.presets import DataDriftPreset


# 12. Przygotowanie danych do raportu Data Drift
# Do analizy driftu wykorzystujemy tylko cechy wejściowe, bez targetu i predykcji.
feature_columns = [f"feature_{i}" for i in range(5)]

reference_data = df_train_loaded[feature_columns]
current_data = df_prod_loaded[feature_columns]


# 13. Utworzenie raportu Data Drift
data_drift_report = Report([
    DataDriftPreset()
])

data_drift_result = data_drift_report.run(
    current_data=current_data,
    reference_data=reference_data
)


# 14. Zapis raportu do pliku HTML
os.makedirs("reports", exist_ok=True)

data_drift_result.save_html("reports/data_drift_report.html")

print("\nRaport Data Drift został zapisany:")
print("reports/data_drift_report.html")

from evidently import Dataset
from evidently import DataDefinition
from evidently import BinaryClassification
from evidently import Report
from evidently.presets import ClassificationPreset

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# 18. Analiza jakości predykcji modelu na danych produkcyjnych

feature_columns = [f"feature_{i}" for i in range(5)]

classification_definition = DataDefinition(
    classification=[
        BinaryClassification(
            target="target",
            prediction_labels="prediction"
        )
    ],
    numerical_columns=feature_columns,
    categorical_columns=["target", "prediction"]
)

current_classification_data = Dataset.from_pandas(
    df_prod_loaded,
    data_definition=classification_definition
)

classification_report = Report([
    ClassificationPreset()
])

classification_result = classification_report.run(
    current_classification_data,
    None
)

os.makedirs("reports", exist_ok=True)

classification_result.save_html(
    "reports/classification_quality_report.html"
)

print("\nRaport jakości klasyfikacji został zapisany:")
print("reports/classification_quality_report.html")


# 19. Dodatkowe wypisanie metryk w konsoli
accuracy = accuracy_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

precision = precision_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

recall = recall_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

f1 = f1_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

print("\n=== JAKOŚĆ PREDYKCJI NA DANYCH PRODUKCYJNYCH ===")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")

# 20. Dodanie predykcji dla zbioru historycznego
df_train_loaded["prediction"] = model.predict(
    df_train_loaded[feature_columns]
)


# 21. Obliczenie metryk dla zbioru historycznego
accuracy_ref = accuracy_score(
    df_train_loaded["target"],
    df_train_loaded["prediction"]
)

precision_ref = precision_score(
    df_train_loaded["target"],
    df_train_loaded["prediction"]
)

recall_ref = recall_score(
    df_train_loaded["target"],
    df_train_loaded["prediction"]
)

f1_ref = f1_score(
    df_train_loaded["target"],
    df_train_loaded["prediction"]
)


# 22. Obliczenie metryk dla zbioru produkcyjnego
accuracy_prod = accuracy_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

precision_prod = precision_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

recall_prod = recall_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)

f1_prod = f1_score(
    df_prod_loaded["target"],
    df_prod_loaded["prediction"]
)


# 23. Porównanie jakości modelu
comparison_df = pd.DataFrame({
    "Zbiór": ["Historyczny", "Produkcyjny"],
    "Accuracy": [accuracy_ref, accuracy_prod],
    "Precision": [precision_ref, precision_prod],
    "Recall": [recall_ref, recall_prod],
    "F1-score": [f1_ref, f1_prod]
})

print("\n=== PORÓWNANIE JAKOŚCI MODELU ===")
print(comparison_df.round(4))

comparison_df.to_csv("reports/model_quality_comparison.csv", index=False)

print("\nPorównanie metryk zapisano do pliku:")
print("reports/model_quality_comparison.csv")

# 24. Raport Evidently porównujący jakość klasyfikacji:
# reference = dane historyczne, current = dane produkcyjne

reference_classification_data = Dataset.from_pandas(
    df_train_loaded,
    data_definition=classification_definition
)

current_classification_data = Dataset.from_pandas(
    df_prod_loaded,
    data_definition=classification_definition
)

classification_comparison_report = Report([
    ClassificationPreset()
])

classification_comparison_result = classification_comparison_report.run(
    current_classification_data,
    reference_classification_data
)

classification_comparison_result.save_html(
    "reports/classification_comparison_report.html"
)

print("\nRaport porównania jakości klasyfikacji został zapisany:")
print("reports/classification_comparison_report.html")