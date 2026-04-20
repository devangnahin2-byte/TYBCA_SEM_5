import sqlite3
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Manage Students", page_icon="💾")

DB_FILE = "college_data.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

st.title("Student Database Operations")

st.subheader("Add New Student")
with st.form("add_student_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=16, max_value=100)
    course = st.selectbox("Course", ["BCA", "BSc IT", "BBA", "BCom", "MCA"])
    submitted = st.form_submit_button("Save to Database")
    
    if submitted:
        if name:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
                conn.commit()
                conn.close()
                st.success(f"Student {name} saved successfully!")
            except Exception as e:
                st.error(f"Database Error! (Did you run 1_5_sqlite_connect.py first?) Detail: {e}")
        else:
            st.error("Name is required!")

st.divider()

st.subheader("Registered Students")
if st.button("Refresh List"):
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM students", conn)
        conn.close()
        
        if df.empty:
            st.info("No students registered yet.")
        else:
            st.dataframe(df)
    except Exception as e:
        st.error("Could not load data. Ensure database is initialized.")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
