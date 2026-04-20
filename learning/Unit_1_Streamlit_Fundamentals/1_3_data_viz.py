import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Unit 1.3: Data Visualization for Analytics")

np.random.seed(42)
data = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100),
    'Sales': np.random.randint(100, 500, size=100),
    'Expenses': np.random.randint(50, 300, size=100),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Groceries'], size=100)
})

st.header("Displaying Datasets")
st.write("Using `st.dataframe` for interactive tables:")
st.dataframe(data.head())

st.sidebar.header("Filter Data")
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

filtered_data = data[data['Category'].isin(selected_category)]
filtered_data = filtered_data.set_index('Date')

st.write(f"Showing data for: {', '.join(selected_category)}")
st.write(f"Total Rows: {len(filtered_data)}")

st.header("Visualizing Analytics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Streamlit Native Line Chart")
    st.line_chart(filtered_data[['Sales', 'Expenses']])

with col2:
    st.subheader("Matplotlib Pyplot Integration")
    fig, ax = plt.subplots()
    filtered_data.groupby('Category')['Sales'].sum().plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax.set_ylabel('Total Sales')
    st.pyplot(fig)


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
