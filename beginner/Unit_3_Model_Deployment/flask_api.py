from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'student_model.joblib')

try:
    model = joblib.load(MODEL_FILE)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route("/", methods=["GET"])
def home():
    return "College Admissions API is running. Send POST requests to /predict"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        model = joblib.load(MODEL_FILE)
    except Exception:
        return jsonify({"error": "Model not found. Run train_model.py first."}), 500
        
    try:
        data = request.json
        math = data.get("Math_Score", 0)
        science = data.get("Science_Score", 0)
        
        pred = model.predict([[math, science]])
        result = "Admitted" if pred[0] == 1 else "Rejected"
        
        return jsonify({
            "Math_Score": math,
            "Science_Score": science,
            "Prediction": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Starting Flask API on port 5000...")
    app.run(port=5000, debug=True)
