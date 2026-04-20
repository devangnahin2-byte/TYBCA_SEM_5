import streamlit as st
import pandas as pd
import numpy as np

st.title("Unit 1.4: Mini Analytics Dashboard")

@st.cache_data
def load_data():
    data = pd.DataFrame({
        'Campaign': [f'Camp_{i}' for i in range(1, 101)],
        'Spend': np.random.uniform(1000, 5000, 100).round(2),
        'Clicks': np.random.randint(500, 2000, 100),
        'Conversions': np.random.randint(10, 200, 100)
    })
    data['Cost_per_Click'] = (data['Spend'] / data['Clicks']).round(2)
    data['Conversion_Rate'] = ((data['Conversions'] / data['Clicks']) * 100).round(2)
    return data

df = load_data()

st.sidebar.header("Dashboard Controls")
min_spend = st.sidebar.slider("Minimum Spend", int(df['Spend'].min()), int(df['Spend'].max()), int(df['Spend'].min()))
filtered_df = df[df['Spend'] >= min_spend]

st.header("Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Campaigns", value=len(filtered_df))
with col2:
    st.metric(label="Total Spend ($)", value=f"${filtered_df['Spend'].sum():,.2f}")
with col3:
    st.metric(label="Total Conversions", value=filtered_df['Conversions'].sum())
with col4:
    avg_cr = filtered_df['Conversion_Rate'].mean()
    st.metric(label="Avg Conversion Rate", value=f"{avg_cr:.2f}%")

st.markdown("---")

st.header("Visual Insights")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Spend vs Conversions (Top 20)")
    top_20 = filtered_df.nlargest(20, 'Conversions')
    top_20_chart = top_20[['Campaign', 'Spend', 'Conversions']].set_index('Campaign')
    st.bar_chart(top_20_chart)

with col_chart2:
    st.subheader("Cost per Click Scatter Trend")
    st.scatter_chart(filtered_df[['Spend', 'Cost_per_Click']])

st.subheader("Raw Data View")
st.dataframe(filtered_df, use_container_width=True)


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
