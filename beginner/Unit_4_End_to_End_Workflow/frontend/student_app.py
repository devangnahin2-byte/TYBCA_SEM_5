import streamlit as st
import requests
import pandas as pd
import subprocess
import sys
import os

st.set_page_config(page_title="Complete Student App", layout="wide")

st.title("Admin Portal: Enrolled Students")

st.markdown("""
This app represents the **Frontend**. It fetches data from our **Backend** (`dummy_api.py`).
""")

st.sidebar.info("🚀 **Cloud Deployment Mode:** Data is now being loaded directly (Backendless).")

st.divider()

if st.button("Fetch Students (Direct Mode)"):
    # Simulated data from the original backend logic
    students_db = [
        {"id": 1, "name": "John Doe", "course": "BCA", "status": "Active"},
        {"id": 2, "name": "Jane Smith", "course": "BBA", "status": "Graduated"},
        {"id": 3, "name": "Sam Wilson", "course": "BSc IT", "status": "Active"}
    ]
    
    try:
        df = pd.DataFrame(students_db)
        st.success("Data loaded successfully!")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
