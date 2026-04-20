from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

try:
    model_path = os.path.join(os.path.dirname(__file__), "iris_model.joblib")
    target_path = os.path.join(os.path.dirname(__file__), "target_names.joblib")
    model = joblib.load(model_path)
    target_names = joblib.load(target_path)
except FileNotFoundError:
    model = None
    print("Model file not found. Please run train_model.py first.")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Iris Prediction API is running."})

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded on server."}), 500
        
    try:
        data = request.get_json()
        
        features = data.get('features')
        
        if not features or len(features) != 4:
            return jsonify({"error": "Invalid input. Expected 4 features."}), 400
            
        features_array = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features_array)[0]
        predicted_class_name = target_names[prediction]
        
        return jsonify({
            "prediction": int(prediction),
            "class_name": predicted_class_name
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
