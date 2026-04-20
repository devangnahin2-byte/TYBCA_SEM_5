import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd
import numpy as np

st.title("Evaluating our Student Predictor")
st.write("How do we know if our model is actually good?")

st.markdown("""
We use **Evaluation Metrics**!
- **Accuracy**: Out of all predictions, how many were correct?
- **Confusion Matrix**: Shows False Positives and False Negatives.
""")

true_labels = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]  # 1 is Pass, 0 is Fail
predictions = [1, 0, 0, 1, 0, 1, 1, 0, 1, 1]  

st.write("### Example Test Results")
results_df = pd.DataFrame({
    "Actual Test Result": ["Pass" if x == 1 else "Fail" for x in true_labels],
    "Model Prediction": ["Pass" if x == 1 else "Fail" for x in predictions]
})
st.dataframe(results_df)

if st.button("Calculate Metrics"):
    acc = accuracy_score(true_labels, predictions)
    cm = confusion_matrix(true_labels, predictions)
    
    st.success(f"**Accuracy:** {acc * 100:.0f}%")
    st.write("Out of 10 students, we predicted 8 correctly!")
    
    st.write("### Confusion Matrix")
    st.write(cm)
    st.caption("Diagonal numbers represent correct predictions.")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
