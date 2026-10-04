import streamlit as st, pandas as pd
st.title("Business Dashboard")
df=st.session_state.get("sales_df")
if df is None: st.info("Upload a sales dataset first.")
else:
    revenue=(df["price"]*df["quantity"]).sum() if "price" in df else None
    c1,c2,c3=st.columns(3); c1.metric("Rows",len(df)); c2.metric("Products",df.product_id.nunique())
    c3.metric("Revenue",f"{revenue:,.2f}" if revenue is not None else "Needs price")
    daily=df.groupby("date")["quantity"].sum(); st.line_chart(daily)
