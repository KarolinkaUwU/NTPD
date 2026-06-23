from pathlib import Path
import joblib
import tensorflow as tf
from sklearn.datasets import load_iris

print("--- Ładowanie zapisanego modelu TensorFlow/Keras ---")

# Ścieżki do zapisanych plików
model_dir = Path(__file__).resolve().parent / "models"
model_path = model_dir / "model_B_v1.keras"
scaler_path = model_dir / "scaler_B_v1.joblib"

# Wczytanie modelu i scalera
loaded_model = tf.keras.models.load_model(model_path)
loaded_scaler = joblib.load(scaler_path)

print("Model został poprawnie wczytany z pliku:")
print(model_path)

print("Scaler został poprawnie wczytany z pliku:")
print(scaler_path)

# Załadowanie zbioru Iris tylko po to, aby odczytać nazwy klas
iris = load_iris()

print("\n--- Predykcja dla przykładowego rekordu ---")

# Przykładowy rekord:
# sepal length, sepal width, petal length, petal width
sample = [[5.1, 3.5, 1.4, 0.2]]

# Przeskalowanie rekordu tym samym scalerem
sample_scaled = loaded_scaler.transform(sample)

# Predykcja prawdopodobieństw klas
prediction_probabilities = loaded_model.predict(sample_scaled)

# Wybór klasy z największym prawdopodobieństwem
predicted_class_number = prediction_probabilities.argmax(axis=1)[0]
predicted_class_name = iris.target_names[predicted_class_number]

print("Przykładowy rekord:")
print(sample)

print("Prawdopodobieństwa klas:")
print(prediction_probabilities)

print("Przewidziany numer klasy:")
print(predicted_class_number)

print("Przewidziana nazwa klasy:")
print(predicted_class_name)