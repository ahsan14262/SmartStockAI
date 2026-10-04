import streamlit as st
from app.analytics.customer import rfm,kmeans_segments,basket_rules
st.title("Customer Insights")
df=st.session_state.get("sales_df")
if df is None: st.info("Upload sales data first."); st.stop()
tab1,tab2=st.tabs(["RFM & K-Means","Market Basket"])
with tab1:
    try:
        x=rfm(df); st.dataframe(kmeans_segments(x),use_container_width=True)
    except Exception as e: st.warning(str(e))
with tab2:
    try:
        rules=basket_rules(df); st.dataframe(rules.head(50),use_container_width=True)
    except Exception as e: st.warning(str(e))
