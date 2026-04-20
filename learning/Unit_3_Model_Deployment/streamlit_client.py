import streamlit as st
import requests

st.title("Unit 3.4: Streamlit Frontend Client")

st.markdown("""
This frontend connects to our Flask API to get predictions.
**Note:** Ensure `flask_api.py` is running in the background.
""")

st.header("Input Features (Iris Dataset)")
sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, value=5.1)
sepal_width = st.number_input("Sepal Width (cm)", min_value=0.0, value=3.5)
petal_length = st.number_input("Petal Length (cm)", min_value=0.0, value=1.4)
petal_width = st.number_input("Petal Width (cm)", min_value=0.0, value=0.2)

import joblib
import os
import numpy as np

if st.button("Get Prediction"):
    features = [sepal_length, sepal_width, petal_length, petal_width]
    
    # Define paths
    model_path = os.path.join(os.path.dirname(__file__), "iris_model.joblib")
    target_path = os.path.join(os.path.dirname(__file__), "target_names.joblib")
    
    try:
        # Load model and names directly
        model = joblib.load(model_path)
        target_names = joblib.load(target_path)
        
        # Prepare input
        features_array = np.array(features).reshape(1, -1)
        
        # Predict
        prediction = model.predict(features_array)[0]
        predicted_class_name = target_names[prediction]
        
        st.success("Prediction calculated successfully (Standalone Mode)!")
        st.write(f"### Predicted Class: **{predicted_class_name.upper()}**")
        st.json({
            "prediction": int(prediction),
            "class_name": predicted_class_name
        })
            
    except Exception as e:
        st.error(f"Failed to load model or predict: {e}")


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
