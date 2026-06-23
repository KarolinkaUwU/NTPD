from pathlib import Path
import joblib
from sklearn.datasets import load_iris

print("--- Ładowanie zapisanego modelu ---")

# Ścieżka do zapisanego modelu
model_path = Path(__file__).resolve().parent / "models" / "model_A_v1.joblib"

# Wczytanie modelu z pliku
loaded_model = joblib.load(model_path)

print("Model został poprawnie wczytany z pliku:")
print(model_path)

# Załadowanie zbioru Iris tylko po to, aby odczytać nazwy klas
iris = load_iris()

print("\n--- Predykcja dla przykładowego rekordu ---")

# Przykładowy rekord:
# sepal length, sepal width, petal length, petal width
sample = [[5.1, 3.5, 1.4, 0.2]]

# Wykonanie predykcji
prediction = loaded_model.predict(sample)

# Odczytanie nazwy przewidzianej klasy
predicted_class_number = prediction[0]
predicted_class_name = iris.target_names[predicted_class_number]

print("Przykładowy rekord:")
print(sample)

print("Przewidziany numer klasy:")
print(predicted_class_number)

print("Przewidziana nazwa klasy:")
print(predicted_class_name)