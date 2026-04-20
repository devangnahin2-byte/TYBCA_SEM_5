import streamlit as st

st.title("Unit 1.2: Interactive User Interfaces")

st.sidebar.header("Sidebar Settings")
st.sidebar.text("Use this area for navigation or app-wide settings.")

col1, col2 = st.columns(2)

with col1:
    st.header("Left Column")
    st.write("This is a container for content on the left.")

with col2:
    st.header("Right Column")
    st.write("This is a container for content on the right.")

st.divider()

st.header("Capturing User Inputs")

user_name = st.text_input("Enter your name:")
user_age = st.slider("Select your age:", min_value=1, max_value=100, value=25)
favorite_color = st.selectbox("Pick a color:", ["Red", "Green", "Blue", "Yellow"])

if 'click_count' not in st.session_state:
    st.session_state.click_count = 0

st.header("Dynamic Outputs")

if st.button("Submit Profile"):
    st.session_state.click_count += 1
    
    st.success(f"Profile Submitted! Welcome {user_name}.")
    
    st.write(f"**Details Captured:**")
    st.write(f"- Age: {user_age}")
    st.write(f"- Favorite Color: {favorite_color}")
    
    st.info(f"You have submitted details {st.session_state.click_count} times during this session.")


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
