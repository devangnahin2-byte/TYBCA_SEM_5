from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "student_marks_model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "student_features.joblib")

try:
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
except FileNotFoundError:
    model = None
    features = []

@app.route('/api/status', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "model_loaded": model is not None})

@app.route('/api/predict/marks', methods=['POST'])
def predict_marks():
    if not model:
        return jsonify({"error": "Model not available"}), 503

    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({"error": "Missing 'features' in payload"}), 400
            
        input_features = data['features']
        
        if len(input_features) != len(features):
            return jsonify({"error": f"Expected {len(features)} features, got {len(input_features)}"}), 400
            
        feature_array = np.array(input_features, dtype=float).reshape(1, -1)
        prediction = model.predict(feature_array)[0]
        prediction = min(max(prediction, 0.0), 100.0)
        
        return jsonify({
            "status": "success",
            "prediction": float(prediction)
        }), 200
        
    except ValueError as ve:
        return jsonify({"error": f"Invalid data type in features: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
