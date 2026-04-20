import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

st.title("Unit 2.1: Unsupervised Learning Algorithms")
st.markdown("### Association Rules: Apriori & FP-Growth")

dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
           ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
           ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]

st.subheader("1. Sample Transaction Dataset")
from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

st.dataframe(df)

min_support = st.slider("Select Minimum Support", 0.1, 1.0, 0.6)

col1, col2 = st.columns(2)

with col1:
    st.subheader("2.1.3 Apriori Algorithm")
    frequent_itemsets_ap = apriori(df, min_support=min_support, use_colnames=True)
    st.write("Frequent Itemsets (Apriori)")
    st.dataframe(frequent_itemsets_ap)

with col2:
    st.subheader("2.1.4 FP-Growth Algorithm")
    frequent_itemsets_fp = fpgrowth(df, min_support=min_support, use_colnames=True)
    st.write("Frequent Itemsets (FP-Growth)")
    st.dataframe(frequent_itemsets_fp)

st.subheader("2.1.2 Association Rules Generation")
min_threshold = st.slider("Select Minimum Confidence Threshold", 0.1, 1.0, 0.7)

if not frequent_itemsets_fp.empty:
    rules = association_rules(frequent_itemsets_fp, metric="confidence", min_threshold=min_threshold)
    st.write("Generated Rules:")
    st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
else:
    st.warning("No frequent itemsets found. Lower the minimum support.")


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
