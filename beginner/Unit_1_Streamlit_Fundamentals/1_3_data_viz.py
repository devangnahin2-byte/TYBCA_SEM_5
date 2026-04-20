import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="College Data Dashboard", page_icon="📊")

st.title("College Admissions Data")
st.write("Visualizing student enrollment across different courses.")

data = {
    "Course": ["BCA", "BSc IT", "BBA", "BCom", "MCA"],
    "Enrolled_Students": [120, 95, 150, 200, 80]
}
df = pd.DataFrame(data)

st.subheader("Enrollment Table")
st.dataframe(df)

st.subheader("Enrollment Chart (Streamlit Bar Chart)")
chart_data = df.set_index("Course")
st.bar_chart(chart_data)

st.subheader("Detailed Chart (Matplotlib)")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(df["Course"], df["Enrolled_Students"], color='skyblue')
ax.set_title("Students per Course")
ax.set_xlabel("Course")
ax.set_ylabel("Number of Students")
for i, v in enumerate(df["Enrolled_Students"]):
    ax.text(i, v + 2, str(v), ha='center')

st.pyplot(fig)

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
