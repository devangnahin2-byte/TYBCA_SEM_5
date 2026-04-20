import streamlit as st

st.set_page_config(page_title="College Management System", page_icon="🎓")

st.title("Welcome to Tech University")
st.header("Student Portal Basics")
st.subheader("Your journey starts here.")

st.write("This is a simple student portal to learn Streamlit basics.")

st.markdown("""
- **Classes** begin next week.
- Make sure to check your *timetable*.
- Contact the admin for any issues.
""")

st.write("### Quick Stats")
st.text("Total Enrolled Students: 1,250")
st.text("Available Courses: 15")
st.text("Faculty Members: 45")

st.info("Tip: Always submit assignments on time!")
st.success("You are successfully logged in.")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
