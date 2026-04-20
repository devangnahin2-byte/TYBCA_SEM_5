import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.title("Unit 1.6: Storing and Retrieving App Results")

def init_history_db():
    conn = sqlite3.connect('analytics_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs
        (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, parameter_x REAL, parameter_y REAL, result REAL)
    ''')
    conn.commit()
    return conn

conn = init_history_db()

st.header("1. Run Complex Analytics")
st.write("Simulate a complex calculation and store the results in the database.")

col1, col2 = st.columns(2)
with col1:
    x_val = st.number_input("Parameter X", value=5.0)
with col2:
    y_val = st.number_input("Parameter Y", value=10.0)

if st.button("Calculate and Save"):
    result = (x_val ** 2) + (y_val * 2.5)
    st.success(f"Calculation Result: {result}")
    
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO runs (timestamp, parameter_x, parameter_y, result) VALUES (?, ?, ?, ?)",
              (timestamp, x_val, y_val, result))
    conn.commit()
    st.info("Result saved to history database.")

st.markdown("---")

st.header("2. Historical Analytics Report")
if st.button("Load History"):
    history_df = pd.read_sql_query("SELECT * FROM runs ORDER BY timestamp DESC", conn)
    
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
        
        st.subheader("Trend over past runs")
        chart_data = history_df[['timestamp', 'result']].set_index('timestamp')
        st.line_chart(chart_data)
        
        st.subheader("Comparison Statistics")
        st.write(f"- Maximum Result Computed: {history_df['result'].max()}")
        st.write(f"- Average X Parameter Used: {history_df['parameter_x'].mean():.2f}")
        st.write(f"- Average Y Parameter Used: {history_df['parameter_y'].mean():.2f}")
    else:
        st.warning("No history found. Run analytics first.")

conn.close()


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
