import streamlit as st
import requests
import json
import os

st.title("🎓 End-to-End ML Project: Student Marks Management System")
st.markdown("This dashboard serves as the frontend for our complete end-to-end Machine Learning pipeline.")

API_URL = "http://localhost:8000/api/predict/marks"
STATUS_URL = "http://localhost:8000/api/status"

import joblib
import numpy as np

# Define local paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "student_marks_model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "student_features.joblib")

st.sidebar.info("🚀 **Cloud Deployment Mode:** Predictive logic is now running directly within Streamlit (Backendless).")

st.markdown("### Student Academic Data")
st.write("Please enter the student's current metrics below to predict their final score:")

col1, col2, col3 = st.columns(3)

with col1:
    study_hours = st.number_input("Total Study Hours", min_value=0, max_value=500, value=120)
with col2:
    attendance = st.number_input("Attendance Percentage", min_value=0, max_value=100, value=85)
with col3:
    midterm_score = st.number_input("Midterm Exam Score", min_value=0, max_value=100, value=75)

st.markdown("---")

if st.button("Predict Final Score", type="primary"):
    features_input = [study_hours, attendance, midterm_score]
    
    with st.spinner("Calculating Prediction..."):
        try:
            # Load model and features directly
            model = joblib.load(MODEL_PATH)
            feature_names = joblib.load(FEATURES_PATH)
            
            # Prepare input
            feature_array = np.array(features_input, dtype=float).reshape(1, -1)
            
            # Predict
            final_score = model.predict(feature_array)[0]
            final_score = min(max(final_score, 0.0), 100.0) # Boundary check
            
            st.success("Prediction successful (Standalone Mode)!")
            st.metric(label="Predicted Final Examination Score", value=f"{final_score:.2f} / 100")
            
            if final_score >= 80:
                st.info("Performance tier: **Distinction** 🌟")
            elif final_score >= 60:
                st.info("Performance tier: **First Class** 👍")
            elif final_score >= 40:
                st.warning("Performance tier: **Pass** 📚")
            else:
                st.error("Performance tier: **Fail** ⚠️ Requires immediate academic intervention.")
                    
        except Exception as e:
            st.error(f"Failed to load model or predict: {e}")


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("st.markdown(\"---\")\nst.markdown(\"### 🎓 Student Learning Section\")")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
