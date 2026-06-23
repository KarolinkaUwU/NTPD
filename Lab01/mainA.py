import pandas as pd
from pathlib import Path
import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# --- Zadanie 1: Załadowanie i analiza danych ---

# Załadowanie wbudowanego zbioru danych Iris z biblioteki scikit-learn
iris = load_iris()

# Dane wejściowe, czyli cechy opisujące kwiaty
X = iris.data

# Etykiety klas, czyli gatunki irysów
y = iris.target

print("--- Załadowanie zbioru danych ---")
print("Zbiór danych został poprawnie załadowany.")
print("Nazwa zbioru: Iris")
print("Liczba próbek:", X.shape[0])
print("Liczba cech:", X.shape[1])
print("Nazwy cech:")
print(iris.feature_names)
print("Nazwy klas:")
print(iris.target_names)

print("\n--- Krótka analiza danych ---")

# Utworzenie tabeli DataFrame na podstawie danych Iris
df = pd.DataFrame(X, columns=iris.feature_names)

# Dodanie kolumny z numerem klasy
df["target"] = y

# Dodanie kolumny z nazwą klasy
df["target_name"] = df["target"].apply(lambda value: iris.target_names[value])

print("\nPierwsze 5 wierszy danych:")
print(df.head())

print("\nRozmiar danych:")
print(df.shape)

print("\nTypy kolumn:")
print(df.dtypes)

print("\nLiczba przykładów w każdej klasie:")
print(df["target_name"].value_counts())

# --- Zadanie 2: Wariant A - scikit-learn ---

print("\n--- Podział danych na zbiór treningowy i testowy ---")

# Podział danych na zbiór treningowy i testowy w proporcji 80% / 20%
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Rozmiar zbioru treningowego X_train:", X_train.shape)
print("Rozmiar zbioru testowego X_test:", X_test.shape)
print("Rozmiar etykiet treningowych y_train:", y_train.shape)
print("Rozmiar etykiet testowych y_test:", y_test.shape)

print("\n--- Wybór algorytmu ML ---")

# Utworzenie modelu regresji logistycznej
model = LogisticRegression(max_iter=1000)

print("Wybrany algorytm:")
print(model)

print("\n--- Trenowanie modelu ---")

# Trenowanie modelu na zbiorze treningowym
model.fit(X_train, y_train)

print("Model został wytrenowany.")

print("\n--- Ewaluacja modelu ---")

# Predykcja na zbiorze testowym
y_pred = model.predict(X_test)

# Obliczenie podstawowych metryk klasyfikacji
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="macro")
recall = recall_score(y_test, y_pred, average="macro")
f1 = f1_score(y_test, y_pred, average="macro")

print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1-score:", round(f1, 4))

print("\nMacierz pomyłek:")
print(confusion_matrix(y_test, y_pred))

print("\nRaport klasyfikacji:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# --- Zadanie 3: Zapisanie i ładowanie modelu (pickle, joblib) ---

print("\n--- Zapis modelu do pliku ---")

# Utworzenie ścieżki do folderu models
model_dir = Path(__file__).resolve().parent / "models"
model_dir.mkdir(exist_ok=True)

# Ścieżka do pliku z modelem
model_path = model_dir / "model_A_v1.joblib"

# Zapisanie modelu do pliku za pomocą joblib
joblib.dump(model, model_path)

print("Model został zapisany do pliku:")
print(model_path)