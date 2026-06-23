from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def train_and_predict():
    """
    Trenuje prosty model LogisticRegression na zbiorze Iris
    i zwraca predykcje oraz prawdziwe etykiety ze zbioru testowego.
    """
    iris = load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    return preds, y_test


def get_accuracy():
    """
    Oblicza dokładność modelu na zbiorze testowym.
    """
    preds, y_test = train_and_predict()
    accuracy = accuracy_score(y_test, preds)

    return accuracy