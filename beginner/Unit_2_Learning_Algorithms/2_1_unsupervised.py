import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Clustering", page_icon="🎯")

st.title("Student Performance Clustering")
st.write("Using Unsupervised Learning (K-Means) to group students based on basic dummy performance data.")

st.info("Scenario: We want to group our students into 'Study Groups' based solely on their exam scores, without knowing the groups in advance.")

np.random.seed(42)
midterms = np.random.randint(40, 100, 50)
finals = midterms + np.random.randint(-15, 15, 50)
finals = np.clip(finals, 0, 100) 

df = pd.DataFrame({"Student_ID": range(1, 51), "Midterm_Score": midterms, "Final_Score": finals})

st.write("### Sample Data")
st.dataframe(df.head())

if st.button("Generate Study Groups"):
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    features = df[["Midterm_Score", "Final_Score"]]
    df["Study_Group"] = kmeans.fit_predict(features)
    
    st.success("Study Groups Assigned!")
    
    fig, ax = plt.subplots()
    scatter = ax.scatter(df["Midterm_Score"], df["Final_Score"], c=df["Study_Group"], cmap='viridis')
    ax.set_xlabel("Midterm Score")
    ax.set_ylabel("Final Score")
    ax.set_title("Student Study Groups")
    st.pyplot(fig)
    
    st.write("Students assigned to groups (sample):")
    st.dataframe(df.head(10))

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
