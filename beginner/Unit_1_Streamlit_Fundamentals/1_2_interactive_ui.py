import streamlit as st

st.set_page_config(page_title="Student Registration", page_icon="📝")

st.title("Student Registration Form")
st.write("Please enter your details below.")

student_name = st.text_input("Full Name", placeholder="e.g., John Doe")
student_age = st.number_input("Age", min_value=16, max_value=60, value=18)

course_selected = st.selectbox(
    "Select Course",
    ["BCA", "BSc IT", "BBA", "BCom"]
)

gender = st.radio(
    "Gender",
    ["Male", "Female", "Other"]
)

has_laptop = st.checkbox("Do you own a laptop?")

if st.button("Submit Registration"):
    if student_name.strip() == "":
        st.error("Please enter your Full Name.")
    else:
        st.success(f"Welcome {student_name}! You have registered for {course_selected}.")
        st.write("### Submitted Details")
        st.write(f"- **Name:** {student_name}")
        st.write(f"- **Age:** {student_age}")
        st.write(f"- **Course:** {course_selected}")
        st.write(f"- **Gender:** {gender}")
        st.write(f"- **Has Laptop:** {'Yes' if has_laptop else 'No'}")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
