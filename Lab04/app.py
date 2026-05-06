from flask import Flask, jsonify, request
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)

# 1. Przygotowanie danych
X = np.array([
    [1, 1],
    [1, 2],
    [2, 1],
    [2, 2],
    [8, 8],
    [8, 9],
    [9, 8],
    [9, 9]
])

y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# 2. Trenowanie modelu
model = LogisticRegression()
model.fit(X, y)

# 3. Endpoint główny
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API działa poprawnie"
    })

# 4. Endpoint predykcji z walidacją
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Brak danych JSON"
        }), 400

    if "feature1" not in data:
        return jsonify({
            "error": "Brak wymaganej wartości: feature1"
        }), 400

    if "feature2" not in data:
        return jsonify({
            "error": "Brak wymaganej wartości: feature2"
        }), 400

    try:
        feature1 = float(data["feature1"])
        feature2 = float(data["feature2"])
    except ValueError:
        return jsonify({
            "error": "feature1 i feature2 muszą być liczbami"
        }), 400

    features = np.array([[feature1, feature2]])
    prediction = model.predict(features)[0]

    return jsonify({
        "input": {
            "feature1": feature1,
            "feature2": feature2
        },
        "prediction": int(prediction)
    })

# 5. Endpoint info
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "model_type": type(model).__name__,
        "number_of_features": X.shape[1],
        "number_of_training_samples": len(X),
        "classes": model.classes_.tolist()
    })

# 6. Endpoint health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })

# 7. Uruchomienie
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
