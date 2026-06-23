import mlflow
import mlflow.sklearn

from sklearn.datasets import load_breast_cancer


# Połączenie z lokalnym serwerem MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")


# Run ID wybranego runu z MLflow
RUN_ID = "b36362fd7bc54a1393b951f38e7afe0a"


# Ścieżka do modelu zapisanego w danym runie
model_uri = f"runs:/{RUN_ID}/model"


# Załadowanie modelu
loaded_model = mlflow.sklearn.load_model(model_uri)

print("Model został poprawnie załadowany z MLflow.")
print(f"Run ID: {RUN_ID}")
print(f"Model URI: {model_uri}")


# Załadowanie przykładowych danych Breast Cancer
data = load_breast_cancer()
X = data.data
y = data.target
target_names = data.target_names


# Wybranie jednej przykładowej próbki
sample = X[0].reshape(1, -1)
true_class = y[0]


# Predykcja dla pojedynczej próbki
predicted_class = loaded_model.predict(sample)[0]


print("\nTest działania modelu na przykładowej próbce:")
print(f"Prawdziwa klasa: {true_class} ({target_names[true_class]})")
print(f"Przewidziana klasa: {predicted_class} ({target_names[predicted_class]})")

# Prawdopodobieństwa klas
predicted_probabilities = loaded_model.predict_proba(sample)[0]

print("\nPrawdopodobieństwa klas:")
for class_index, probability in enumerate(predicted_probabilities):
    print(f"Klasa {class_index} ({target_names[class_index]}): {probability:.4f}")