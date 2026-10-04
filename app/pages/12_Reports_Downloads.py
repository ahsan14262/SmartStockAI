import streamlit as st
from app.exports.reporting import csv_bytes,xlsx_bytes,docx_bytes,pdf_bytes
st.title("Reports & Downloads")
df=st.session_state.get("sales_df")
if df is None: st.info("Upload sales data first."); st.stop()
summary=f"Rows: {len(df)} | Products: {df.product_id.nunique()} | Period: {df.date.min()} to {df.date.max()}"
st.write(summary)
st.download_button("CSV",csv_bytes(df),"smart_stock_report.csv","text/csv")
st.download_button("Excel",xlsx_bytes(df),"smart_stock_report.xlsx")
st.download_button("Word",docx_bytes("Smart Stock Report",[summary]),"smart_stock_report.docx")
st.download_button("PDF",pdf_bytes("Smart Stock Report",[summary]),"smart_stock_report.pdf")
