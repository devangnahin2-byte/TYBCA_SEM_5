import sqlite3
import streamlit as st
import os

st.title("Database Connection Setup")
st.write("This simple script ensures our SQLite database is properly created for the College System.")

DB_FILE = "college_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT
        )
    ''')
    conn.commit()
    conn.close()

if st.button("Initialize College Database"):
    try:
        init_db()
        st.success(f"Database setup successfully! File created at: {os.path.abspath(DB_FILE)}")
    except Exception as e:
        st.error(f"Failed to setup database: {e}")

st.info("Click the button above to make sure the database file exists before moving to the next example.")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
