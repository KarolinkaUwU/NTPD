import mlflow
import mlflow.sklearn

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Połączenie z lokalnym serwerem MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Default")


# 1. Załadowanie danych Breast Cancer
data = load_breast_cancer()
X = data.data
y = data.target


# 2. Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 3. Lista różnych wartości hiperparametru C
C_values = [0.01, 0.1, 1.0, 10.0]

max_iter = 1000
solver = "lbfgs"


# 4. Pętla wykonująca kilka eksperymentów MLflow
for C in C_values:

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            C=C,
            max_iter=max_iter,
            solver=solver,
            random_state=42
        ))
    ])

    with mlflow.start_run(run_name=f"logistic_regression_C_{C}"):

        # Trenowanie modelu
        model.fit(X_train, y_train)

        # Predykcja na zbiorze testowym
        y_pred = model.predict(X_test)

        # Obliczenie metryk
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Logowanie parametrów
        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("dataset", "Breast Cancer Wisconsin")
        mlflow.log_param("C", C)
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("solver", solver)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)

        # Logowanie metryk
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # Logowanie modelu
        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name="BreastCancer_LogisticRegression"
        )

        # Wyniki w konsoli
        print(f"Run dla C = {C}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-score:  {f1:.4f}")
        print("-" * 40)

print("Wszystkie eksperymenty zakończone.")