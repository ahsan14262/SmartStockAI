import streamlit as st
from app.core.config import settings
from app.core.ui import inject_brand_css
from app.db.session import init_db

st.set_page_config(page_title="Smart Stock Agent", page_icon="📦", layout="wide")
inject_brand_css()
init_db()

st.title("📦 Smart Stock Agent")
st.subheader("Buy the right product • at the right time • in the right quantity")
st.write(
    "A retail decision-support workspace combining demand forecasting, inventory optimization, "
    "customer analytics, grounded business Q&A, approvals, and reporting."
)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Forecasting", "7–90 days")
c2.metric("Inventory", "EOQ / ROP")
c3.metric("Retrieval", "Hybrid RAG")
c4.metric("Governance", "RBAC + Audit")
st.info("Start with **Sign In & Onboarding**, then use **Upload & Data Quality** to load sample or real sales data.")
st.caption(f"Environment: {settings.app_env} | Local tenant: {settings.default_tenant_id}")
