from pathlib import Path
import pandas as pd
import streamlit as st

st.title("Business Dashboard")

df = st.session_state.get("sales_df")
data_source = "Uploaded dataset"

if df is None:
    sample_path = Path("data/sample/sales.csv")
    if sample_path.exists():
        try:
            df = pd.read_csv(sample_path)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
            st.session_state["sales_df"] = df
            data_source = "Sample sales dataset"
            st.info("No uploaded dataset found. Showing the bundled sample sales data.")
        except Exception as exc:
            st.error(f"Could not load sample sales data: {exc}")
            st.stop()
    else:
        st.warning("No sales dataset is available. Open Upload & Data Quality to upload one.")
        st.stop()

st.caption(f"Data source: {data_source}")

required = {"product_id", "quantity"}
missing = required - set(df.columns)
if missing:
    st.error("Dataset is missing required columns: " + ", ".join(sorted(missing)))
    st.stop()

revenue = None
if {"price", "quantity"}.issubset(df.columns):
    revenue = (pd.to_numeric(df["price"], errors="coerce").fillna(0) *
               pd.to_numeric(df["quantity"], errors="coerce").fillna(0)).sum()

c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Products", f"{df['product_id'].nunique():,}")
c3.metric("Revenue", f"{revenue:,.2f}" if revenue is not None else "Needs price")

if "date" in df.columns:
    chart_df = df.copy()
    chart_df["date"] = pd.to_datetime(chart_df["date"], errors="coerce")
    chart_df["quantity"] = pd.to_numeric(chart_df["quantity"], errors="coerce").fillna(0)
    daily = chart_df.dropna(subset=["date"]).groupby("date")["quantity"].sum()
    if not daily.empty:
        st.subheader("Daily Sales")
        st.line_chart(daily)

st.subheader("Sales Preview")
st.dataframe(df.head(100), use_container_width=True)
