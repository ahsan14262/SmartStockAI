from pathlib import Path
import pandas as pd
import streamlit as st

from app.analytics.customer import rfm, kmeans_segments, basket_rules, churn_labels

st.title("Customer Insights")

df = st.session_state.get("sales_df")
data_source = "Uploaded/loaded dataset"

if df is None or df.empty:
    sample_path = Path("data/sample/sales.csv")
    if sample_path.exists():
        try:
            df = pd.read_csv(sample_path)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
            st.session_state.sales_df = df
            data_source = "Sample sales dataset"
            st.info("No uploaded dataset found. Showing customer insights from the bundled sample data.")
        except Exception as e:
            st.error(f"Could not load sample sales data: {e}")
            st.stop()
    else:
        st.warning("No sales data is available. Use Upload & Data Quality first.")
        st.stop()
else:
    if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

st.caption(f"Data source: {data_source}")

t1, t2, t3 = st.tabs(["RFM & K-Means", "Churn definition", "Market Basket"])

with t1:
    try:
        result = kmeans_segments(rfm(df))
        c1, c2 = st.columns(2)
        c1.metric("Customers", f"{result['customer_id'].nunique():,}")
        c2.metric("Segments", f"{result['segment'].nunique():,}")
        st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.warning(str(e))
        st.caption("Needs stable customer IDs, transaction IDs, price and repeat-purchase history.")

with t2:
    try:
        inactivity = st.number_input("Inactivity threshold (days)", 30, 365, 60)
        horizon = st.number_input("Prediction horizon (days)", 7, 180, 30)
        labels, meta = churn_labels(df, inactivity, horizon)
        st.json(meta)
        if not labels.empty:
            c1, c2 = st.columns(2)
            c1.metric("Evaluated customers", f"{len(labels):,}")
            c2.metric("Churned", f"{int(labels['churned'].sum()):,}")
        st.dataframe(labels, use_container_width=True)
        st.caption("These are leakage-safe historical labels for evaluation, not a production churn probability model yet.")
    except Exception as e:
        st.warning(str(e))

with t3:
    try:
        rules = basket_rules(df).head(50)
        if rules.empty:
            st.info("No association rules met the current support/confidence thresholds.")
        else:
            st.dataframe(rules, use_container_width=True)
    except Exception as e:
        st.warning(str(e))
        st.caption("Needs transaction-level item groupings. Anonymous transactions can support baskets but not customer RFM/churn.")
