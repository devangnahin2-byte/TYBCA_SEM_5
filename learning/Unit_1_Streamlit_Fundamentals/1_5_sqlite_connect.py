import streamlit as st
import sqlite3
import pandas as pd

st.title("Unit 1.5: SQLite Integration")

def init_db():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, department TEXT, salary REAL)
    ''')
    conn.commit()
    return conn

conn = init_db()

st.header("Employee Management (CRUD)")

with st.form("add_employee_form"):
    st.subheader("Add New Employee")
    emp_name = st.text_input("Name")
    emp_dept = st.selectbox("Department", ["IT", "HR", "Finance", "Sales"])
    emp_salary = st.number_input("Salary", min_value=10000)
    
    submitted = st.form_submit_button("Add Record")
    if submitted and emp_name:
        c = conn.cursor()
        c.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", 
                  (emp_name, emp_dept, emp_salary))
        conn.commit()
        st.success(f"Added {emp_name} to database!")

delete_id = st.text_input("Enter ID of employee to delete:")
if st.button("Delete"):
    if delete_id:
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE id=?", (delete_id,))
        conn.commit()
        st.warning(f"Deleted record with ID {delete_id}")

st.markdown("---")

st.header("Filter & Query Engine")
search_dept = st.selectbox("Filter by Department:", ["All", "IT", "HR", "Finance", "Sales"])

query = "SELECT * FROM employees"
if search_dept != "All":
    query += f" WHERE department = '{search_dept}'"

df = pd.read_sql_query(query, conn)

st.write("### Database Records")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No records found.")
    
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
