import streamlit as st
st.title("Finance")
df=st.session_state.get("sales_df")
if df is None: st.info("Upload sales data first.")
elif {"price","cost","quantity"}.issubset(df.columns):
    rev=(df.price*df.quantity).sum(); cogs=(df.cost*df.quantity).sum()
    c1,c2,c3=st.columns(3); c1.metric("Revenue",f"{rev:,.2f}"); c2.metric("COGS",f"{cogs:,.2f}"); c3.metric("Gross profit",f"{rev-cogs:,.2f}")
else: st.warning("Finance summary needs price, cost and quantity.")
