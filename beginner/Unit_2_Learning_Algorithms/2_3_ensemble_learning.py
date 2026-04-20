import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Predict Student Success", page_icon="🌳")

st.title("Student Success Prediction")
st.write("Using Ensemble Learning (Random Forest) to predict if a student passes or fails.")

st.write("### Training Data")
data = {
    "Study_Hours_Per_Week": [10, 20, 5, 25, 30, 2, 15, 8],
    "Attendance_Percent":   [80, 95, 50, 90, 99, 40, 85, 60],
    "Passed":               ["Yes", "Yes", "No", "Yes", "Yes", "No", "Yes", "No"]
}
df = pd.DataFrame(data)
st.dataframe(df)

st.write("### Try It Yourself")
study_hours = st.slider("Study Hours Per Week", 0, 40, 15)
attendance = st.slider("Attendance %", 0, 100, 75)

if st.button("Predict Outcome"):
    y = df["Passed"].apply(lambda x: 1 if x == "Yes" else 0)
    X = df[["Study_Hours_Per_Week", "Attendance_Percent"]]
    
    rf_model = RandomForestClassifier(n_estimators=10, random_state=42)
    rf_model.fit(X, y)
    
    user_input = pd.DataFrame({
        "Study_Hours_Per_Week": [study_hours],
        "Attendance_Percent": [attendance]
    })
    
    prediction_num = rf_model.predict(user_input)[0]
    
    if prediction_num == 1:
        st.success("Prediction: **Pass** 🎉 Keep it up!")
    else:
        st.error("Prediction: **Fail** ⚠️ You might need to study more.")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
