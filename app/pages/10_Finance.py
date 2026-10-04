from pathlib import Path
import pandas as pd
import streamlit as st

st.title("Finance")

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
            st.info("No uploaded dataset found. Showing finance metrics from the bundled sample data.")
        except Exception as e:
            st.error(f"Could not load sample sales data: {e}")
            st.stop()
    else:
        st.warning("No sales data is available. Use Upload & Data Quality first.")
        st.stop()

st.caption(f"Data source: {data_source}")

required = {"price", "cost", "quantity"}
if required.issubset(df.columns):
    work = df.copy()
    for col in required:
        work[col] = pd.to_numeric(work[col], errors="coerce").fillna(0)

    revenue = (work["price"] * work["quantity"]).sum()
    cogs = (work["cost"] * work["quantity"]).sum()
    gross_profit = revenue - cogs
    margin = (gross_profit / revenue * 100) if revenue else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", f"{revenue:,.2f}")
    c2.metric("COGS", f"{cogs:,.2f}")
    c3.metric("Gross Profit", f"{gross_profit:,.2f}")
    c4.metric("Gross Margin", f"{margin:.1f}%")

    if "date" in work.columns:
        work["date"] = pd.to_datetime(work["date"], errors="coerce")
        work["revenue"] = work["price"] * work["quantity"]
        work["cogs"] = work["cost"] * work["quantity"]
        work["gross_profit"] = work["revenue"] - work["cogs"]
        daily = work.dropna(subset=["date"]).groupby("date")[["revenue", "cogs", "gross_profit"]].sum()
        if not daily.empty:
            st.subheader("Financial Performance")
            st.line_chart(daily)

    if "product_id" in work.columns:
        product = work.assign(
            revenue=work["price"] * work["quantity"],
            gross_profit=(work["price"] - work["cost"]) * work["quantity"],
        ).groupby("product_id", as_index=False)[["revenue", "gross_profit"]].sum()
        product = product.sort_values("gross_profit", ascending=False)
        st.subheader("Profit by Product")
        st.dataframe(product, use_container_width=True)
else:
    missing = sorted(required - set(df.columns))
    st.warning("Finance summary needs price, cost and quantity.")
    st.caption("Missing columns: " + ", ".join(missing))
