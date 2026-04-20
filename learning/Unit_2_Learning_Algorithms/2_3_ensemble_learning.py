import streamlit as st
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score

st.title("Unit 2.3: Ensemble Learning")

st.markdown("""
Ensemble learning combines predictions from multiple machine learning algorithms to make more accurate predictions than any individual model.
""")

@st.cache_data
def get_data():
    data = load_wine()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df, data.target_names

df, target_names = get_data()

st.subheader("Wine Classification Dataset")
st.dataframe(df.head())

st.subheader("Compare Ensemble Classifiers")

X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Random Forest (Bagging)")
    rf_estimators = st.slider("Number of Trees (RF)", 10, 200, 50)
    
    rf = RandomForestClassifier(n_estimators=rf_estimators, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    
    st.success(f"Random Forest Accuracy: {rf_acc:.4f}")

with col2:
    st.markdown("### 2. Gradient Boosting (Boosting)")
    gb_estimators = st.slider("Number of Trees (GB)", 10, 200, 50)
    
    gb = GradientBoostingClassifier(n_estimators=gb_estimators, random_state=42)
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)
    gb_acc = accuracy_score(y_test, gb_pred)
    
    st.success(f"Gradient Boosting Accuracy: {gb_acc:.4f}")

st.markdown("""
- **Bagging (e.g., Random Forest)**: Builds multiple independent models (decision trees) parallelly and averages their predictions to reduce variance and prevent overfitting.
- **Boosting (e.g., Gradient Boosting)**: Builds models sequentially, where each new model tries to correct the errors of the previous ones, effectively reducing bias.
""")


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
