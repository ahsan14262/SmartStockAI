import streamlit as st
st.title("Automation & Approvals")
st.write("Planned controlled workflows: scheduled forecasts, reorder alerts, purchase drafts, expiry reviews, price proposals, customer campaigns, finance summaries and market research.")
kind=st.selectbox("Automation",["Scheduled forecast","Reorder alert","Expiry review","Price proposal","Market research"])
enabled=st.toggle("Enabled")
st.json({"kind":kind,"enabled":enabled,"approval_required":kind in ["Price proposal"],"status":"configuration draft"})
