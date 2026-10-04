import streamlit as st
def inject_brand_css():
    st.markdown("""<style>
    :root{--navy:#0F172A;--teal:#0F766E;--amber:#F59E0B}
    .stApp{background:#F8FAFC}
    h1,h2,h3{color:#0F172A}
    div[data-testid="stMetric"]{background:white;border:1px solid #E2E8F0;padding:14px;border-radius:12px}
    .stButton>button{border-radius:9px}
    </style>""", unsafe_allow_html=True)
