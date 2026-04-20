import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Mini Student Dashboard", page_icon="🏫")

st.title("🎓 College System Mini Dashboard")

st.write("### Quick Overview")
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Students", value="560", delta="12 This week")
col2.metric(label="Active Courses", value="8", delta="0")
col3.metric(label="Average Attendance", value="85%", delta="-2%")

st.divider()

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("Add Notice")
    notice_title = st.text_input("Notice Title")
    notice_body = st.text_area("Notice Details")
    priority = st.selectbox("Priority", ["Normal", "High", "Critical"])
    if st.button("Post Notice"):
        st.success(f"Notice '{notice_title}' posted securely!")

with right_col:
    st.subheader("Recent Admissions")
    recent_students = pd.DataFrame({
        "Roll No": [101, 102, 103, 104],
        "Name": ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince"],
        "Course": ["BCA", "BBA", "BCA", "BCom"],
        "Join Date": ["2023-08-01", "2023-08-02", "2023-08-03", "2023-08-05"]
    })
    st.dataframe(recent_students, use_container_width=True)

    st.info("Dashboard auto-updates when new data is added.")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
