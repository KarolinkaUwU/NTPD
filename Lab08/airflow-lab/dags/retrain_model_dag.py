from pathlib import Path

import pendulum
from airflow.sdk import dag, task


BASE_DIR = Path("/opt/airflow")
DATA_PATH = BASE_DIR / "data" / "new_data.csv"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
PRODUCTION_DIR = MODELS_DIR / "production"
PRODUCTION_MODEL_PATH = PRODUCTION_DIR / "current_model.pkl"


@dag(
    dag_id="retrain_model",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["lab08", "retraining", "ml"],
)
def retrain_model():

    @task
    def prepare_data():
        import pandas as pd
        from sklearn.datasets import make_classification

        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        X, y = make_classification(
            n_samples=500,
            n_features=5,
            n_informative=4,
            n_redundant=1,
            random_state=42
        )

        df = pd.DataFrame(
            X,
            columns=[f"feature_{i}" for i in range(5)]
        )

        df["target"] = y
        df.to_csv(DATA_PATH, index=False)

        print(f"Zapisano nowy zbiór danych: {DATA_PATH}")
        print(f"Liczba rekordów: {len(df)}")

        return str(DATA_PATH)

    @task
    def train_and_validate_model(data_path: str):
        import datetime
        import joblib
        import pandas as pd

        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split

        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)

        df = pd.read_csv(data_path)

        X = df.drop("target", axis=1)
        y = df["target"]

        X_train, X_val, y_train, y_val = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        # Trenowanie nowej wersji modelu
        new_model = RandomForestClassifier(random_state=42)
        new_model.fit(X_train, y_train)

        # Walidacja nowej wersji modelu
        new_predictions = new_model.predict(X_val)
        new_accuracy = accuracy_score(y_val, new_predictions)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        new_model_path = MODELS_DIR / f"rf_model_{timestamp}.pkl"
        report_path = REPORTS_DIR / f"validation_report_{timestamp}.txt"

        # Zapis nowego modelu jako wersji archiwalnej
        joblib.dump(new_model, new_model_path)

        # Porównanie z aktualnym modelem produkcyjnym, jeśli istnieje
        old_accuracy = None
        comparison_result = "Brak wcześniejszego modelu produkcyjnego do porównania."

        if PRODUCTION_MODEL_PATH.exists():
            old_model = joblib.load(PRODUCTION_MODEL_PATH)
            old_predictions = old_model.predict(X_val)
            old_accuracy = accuracy_score(y_val, old_predictions)

            if new_accuracy > old_accuracy:
                comparison_result = "Nowy model osiągnął lepszy wynik niż model produkcyjny."
            elif new_accuracy == old_accuracy:
                comparison_result = "Nowy model osiągnął taki sam wynik jak model produkcyjny."
            else:
                comparison_result = "Nowy model osiągnął gorszy wynik niż model produkcyjny."

        # Zapis raportu walidacji
        with open(report_path, "w", encoding="utf-8") as file:
            file.write("Raport walidacji modelu\n")
            file.write("Model: RandomForestClassifier\n")
            file.write(f"Nowy model: {new_model_path}\n")
            file.write(f"Accuracy nowego modelu: {new_accuracy:.4f}\n")

            if old_accuracy is not None:
                file.write(f"Model produkcyjny: {PRODUCTION_MODEL_PATH}\n")
                file.write(f"Accuracy starego modelu: {old_accuracy:.4f}\n")
            else:
                file.write("Model produkcyjny: brak\n")
                file.write("Accuracy starego modelu: brak\n")

            file.write(f"Wynik porównania: {comparison_result}\n")

        print(f"Nowy model zapisano jako: {new_model_path}")
        print(f"Raport walidacji zapisano jako: {report_path}")
        print(f"Accuracy nowego modelu: {new_accuracy:.4f}")

        if old_accuracy is not None:
            print(f"Accuracy starego modelu produkcyjnego: {old_accuracy:.4f}")
        else:
            print("Brak starego modelu produkcyjnego do porównania.")

        print(comparison_result)

        return {
            "new_model_path": str(new_model_path),
            "production_model_path": str(PRODUCTION_MODEL_PATH),
            "new_accuracy": round(float(new_accuracy), 4),
            "old_accuracy": None if old_accuracy is None else round(float(old_accuracy), 4),
            "comparison_result": comparison_result,
        }

    @task
    def update_production_model(validation_result: dict):
        import shutil
        import datetime

        new_model_path = Path(validation_result["new_model_path"])
        production_model_path = Path(validation_result["production_model_path"])

        new_accuracy = validation_result["new_accuracy"]
        old_accuracy = validation_result["old_accuracy"]

        PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        if old_accuracy is None:
            shutil.copy2(new_model_path, production_model_path)
            decision = (
                "Brak wcześniejszego modelu produkcyjnego. "
                "Nowy model ustawiono jako model produkcyjny."
            )

        elif new_accuracy > old_accuracy:
            shutil.copy2(new_model_path, production_model_path)
            decision = (
                f"Nowy model jest lepszy. "
                f"Accuracy nowego modelu: {new_accuracy}, "
                f"accuracy starego modelu: {old_accuracy}. "
                f"Model produkcyjny został podmieniony."
            )

        else:
            decision = (
                f"Nowy model nie jest lepszy. "
                f"Accuracy nowego modelu: {new_accuracy}, "
                f"accuracy starego modelu: {old_accuracy}. "
                f"Model produkcyjny nie został podmieniony. "
                f"Nowy model pozostaje tylko jako model archiwalny."
            )

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        decision_report_path = REPORTS_DIR / f"production_update_decision_{timestamp}.txt"

        with open(decision_report_path, "w", encoding="utf-8") as file:
            file.write("Decyzja o aktualizacji modelu produkcyjnego\n")
            file.write(f"Nowy model: {new_model_path}\n")
            file.write(f"Model produkcyjny: {production_model_path}\n")
            file.write(f"Accuracy nowego modelu: {new_accuracy}\n")
            file.write(f"Accuracy starego modelu: {old_accuracy}\n")
            file.write(f"Decyzja: {decision}\n")

        print(decision)
        print(f"Aktualny model produkcyjny: {production_model_path}")
        print(f"Raport decyzji zapisano jako: {decision_report_path}")

        return decision

    data_path = prepare_data()
    validation_result = train_and_validate_model(data_path)
    update_production_model(validation_result)


retrain_model()