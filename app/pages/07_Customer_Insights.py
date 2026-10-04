import streamlit as st
from app.analytics.customer import rfm,kmeans_segments,basket_rules,churn_labels
st.title("Customer Insights"); df=st.session_state.get("sales_df")
if df is None: st.info("Upload sales data first."); st.stop()
t1,t2,t3=st.tabs(["RFM & K-Means","Churn definition","Market Basket"])
with t1:
    try: st.dataframe(kmeans_segments(rfm(df)),use_container_width=True)
    except Exception as e: st.warning(str(e)); st.caption("Needs stable customer IDs, transaction IDs, price and repeat-purchase history.")
with t2:
    try:
        inactivity=st.number_input("Inactivity threshold (days)",30,365,60); horizon=st.number_input("Prediction horizon (days)",7,180,30)
        labels,meta=churn_labels(df,inactivity,horizon); st.json(meta); st.dataframe(labels,use_container_width=True)
        st.caption("These are leakage-safe historical labels for evaluation, not a production churn probability model yet.")
    except Exception as e: st.warning(str(e))
with t3:
    try: st.dataframe(basket_rules(df).head(50),use_container_width=True)
    except Exception as e: st.warning(str(e)); st.caption("Needs transaction-level item groupings. Anonymous transactions can support baskets but not customer RFM/churn.")
