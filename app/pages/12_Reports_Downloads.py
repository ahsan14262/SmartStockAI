from pathlib import Path
import pandas as pd
import streamlit as st

from app.exports.reporting import csv_bytes, xlsx_bytes, docx_bytes, pdf_bytes

st.title("Reports & Downloads")

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
            st.info("No uploaded dataset found. Reports are using the bundled sample sales data.")
        except Exception as e:
            st.error(f"Could not load sample sales data: {e}")
            st.stop()
    else:
        st.warning("No sales data is available. Use Upload & Data Quality first.")
        st.stop()

st.caption(f"Data source: {data_source}")

products = df["product_id"].nunique() if "product_id" in df.columns else "N/A"
if "date" in df.columns:
    dates = pd.to_datetime(df["date"], errors="coerce").dropna()
    period = f"{dates.min().date()} to {dates.max().date()}" if not dates.empty else "N/A"
else:
    period = "N/A"

summary = f"Rows: {len(df):,} | Products: {products} | Period: {period}"
st.subheader("Report Summary")
st.write(summary)

c1, c2 = st.columns(2)
with c1:
    st.download_button("⬇️ Download CSV", csv_bytes(df), "smart_stock_report.csv", "text/csv", use_container_width=True)
    st.download_button("⬇️ Download Word", docx_bytes("Smart Stock Report", [summary]), "smart_stock_report.docx", use_container_width=True)
with c2:
    st.download_button("⬇️ Download Excel", xlsx_bytes(df), "smart_stock_report.xlsx", use_container_width=True)
    st.download_button("⬇️ Download PDF", pdf_bytes("Smart Stock Report", [summary]), "smart_stock_report.pdf", use_container_width=True)

st.subheader("Data Preview")
st.dataframe(df.head(100), use_container_width=True)
