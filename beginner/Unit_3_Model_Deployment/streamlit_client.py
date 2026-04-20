import streamlit as st
import requests
import subprocess
import sys
import os

st.set_page_config(page_title="Admissions Predictor UI", page_icon="🎓")

st.title("Admissions Status Checker")
st.write("This app sends data to our Flask API behind the scenes.")

st.info("Make sure you are running 'flask_api.py' in a separate terminal!")

import joblib
import numpy as np

st.sidebar.info("🚀 **Cloud Deployment Mode:** Predictive logic is now running directly within Streamlit (Backendless).")

st.divider()

math_score = st.number_input("Enter Math Score", min_value=0, max_value=100, value=75)
science_score = st.number_input("Enter Science Score", min_value=0, max_value=100, value=75)

if st.button("Check Admission Status"):
    model_path = os.path.join(os.path.dirname(__file__), "student_model.joblib")
    
    try:
        # Load model directly
        model = joblib.load(model_path)
        
        # Predict
        pred = model.predict([[math_score, science_score]])
        result = "Admitted" if pred[0] == 1 else "Rejected"
        
        if result == "Admitted":
            st.success("🎉 You are predicted to be ADMITTED!")
        else:
            st.error("⚠️ Prediction stands at: REJECTED.")
            
    except Exception as e:
        st.error(f"Failed to load model or predict: {e}")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
