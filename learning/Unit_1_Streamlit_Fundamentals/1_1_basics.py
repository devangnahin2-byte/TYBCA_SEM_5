import streamlit as st


st.title("Unit 1.1: Streamlit Basics")

st.markdown("""
Streamlit is an open-source Python library that makes it easy to build custom web apps for machine learning and data science.
""")

st.write("Hello World! This is a simple application.")

st.info("To run this app, use the command: `streamlit run 1_1_basics.py` in your terminal.")

st.header("Execution Flow Example")
st.markdown("""
Streamlit runs the script from top to bottom every time you interact with it. 
Try clicking the button below to see how it works!
""")

if st.button("Click Me to Rerun App!"):
    st.success("App has been re-run. Notice how Streamlit executes everything from the top down.")
    st.balloons()


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
