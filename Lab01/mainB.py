import pandas as pd
import tensorflow as tf
from pathlib import Path
import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

# --- Zadanie 2: Wariant B - TensorFlow / Keras ---

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

print("\n--- Standaryzacja danych ---")

# Standaryzacja cech numerycznych
# Sieci neuronowe zwykle uczą się stabilniej, gdy dane są przeskalowane
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Dane zostały przeskalowane za pomocą StandardScaler.")

print("\n--- Tworzenie sieci neuronowej ---")

# Ustawienie ziarna losowości dla bardziej powtarzalnych wyników
tf.random.set_seed(42)

# Liczba cech wejściowych i liczba klas
n_features = X_train_scaled.shape[1]
n_classes = len(iris.target_names)

# Stworzenie prostej sieci neuronowej z warstwami Dense
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(n_features,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(n_classes, activation="softmax")
])

print("Utworzono model sieci neuronowej:")
model.summary()

print("\n--- Konfiguracja procesu uczenia ---")

# Konfiguracja modelu
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("Model został skompilowany.")
print("Optimizer: adam")
print("Loss: sparse_categorical_crossentropy")
print("Metrics: accuracy")

print("\n--- Trenowanie modelu ---")

# Trenowanie modelu
history = model.fit(
    X_train_scaled,
    y_train,
    epochs=50,
    batch_size=8,
    validation_split=0.2,
    verbose=1
)

print("\nModel został wytrenowany.")

print("\n--- Ewaluacja modelu ---")

# Ewaluacja modelu na zbiorze testowym
test_loss, test_accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)

print("Test loss:", round(test_loss, 4))
print("Test accuracy:", round(test_accuracy, 4))

print("\n--- Predykcja dla przykładowego rekordu ---")

# Przykładowy rekord:
# sepal length, sepal width, petal length, petal width
sample = [[5.1, 3.5, 1.4, 0.2]]

# Przeskalowanie przykładowego rekordu tym samym scalerem
sample_scaled = scaler.transform(sample)

# Predykcja prawdopodobieństw klas
prediction_probabilities = model.predict(sample_scaled)

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

# --- Zadanie 3: Zapisanie modelu TensorFlow/Keras ---

print("\n--- Zapis modelu do pliku ---")

# Utworzenie ścieżki do folderu models
model_dir = Path(__file__).resolve().parent / "models"
model_dir.mkdir(exist_ok=True)

# Ścieżki do plików
model_path = model_dir / "model_B_v1.keras"
scaler_path = model_dir / "scaler_B_v1.joblib"

# Zapisanie modelu Keras
model.save(model_path)

# Zapisanie scalera, który był używany do standaryzacji danych
joblib.dump(scaler, scaler_path)

print("Model TensorFlow/Keras został zapisany do pliku:")
print(model_path)

print("Scaler został zapisany do pliku:")
print(scaler_path)