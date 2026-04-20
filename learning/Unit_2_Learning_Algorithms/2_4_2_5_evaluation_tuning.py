import streamlit as st
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Unit 2.4 & 2.5: Evaluation Metrics and Parameter Tuning")

@st.cache_data
def get_data():
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df, data.target_names, data.data, data.target

df, target_names, X, y = get_data()
st.write("Dataset: Breast Cancer Wisconsin")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

st.header("1. Model Training & Parameter Tuning (GridSearchCV)")
st.write("We will tune a Support Vector Classifier (SVC).")

col1, col2 = st.columns(2)
with col1:
    c_values = st.multiselect("Select C parameters to test:", [0.1, 1, 10, 100], default=[0.1, 1, 10])
with col2:
    kernel_values = st.multiselect("Select Kernels to test:", ['linear', 'rbf'], default=['linear', 'rbf'])

if st.button("Run Grid Search"):
    with st.spinner("Tuning parameters..."):
        param_grid = {'C': c_values, 'kernel': kernel_values}
        grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=0, cv=3)
        grid.fit(X_train, y_train)
        
        st.success("GridSearch Complete!")
        st.write(f"**Best Parameters Found:** `{grid.best_params_}`")
        
        grid_predictions = grid.predict(X_test)
        
        st.markdown("---")
        st.header("2. Performance Matrix Evaluation")
        
        col_eval1, col_eval2 = st.columns(2)
        
        with col_eval1:
            st.subheader("Classification Report")
            report = classification_report(y_test, grid_predictions, target_names=target_names, output_dict=True)
            st.dataframe(pd.DataFrame(report).transpose())
            st.metric("Overall Accuracy", f"{accuracy_score(y_test, grid_predictions):.4f}")
            
        with col_eval2:
            st.subheader("Confusion Matrix")
            cm = confusion_matrix(y_test, grid_predictions)
            fig, ax = plt.subplots(figsize=(4,3))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                        xticklabels=target_names, yticklabels=target_names)
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            st.pyplot(fig)


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
