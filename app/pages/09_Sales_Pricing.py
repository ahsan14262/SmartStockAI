import streamlit as st
from app.analytics.pricing import price_recommendation
st.title("Sales & Pricing")
price=st.number_input("Current price",0.01,value=100.0); cost=st.number_input("Unit cost",0.0,value=70.0)
margin=st.slider("Target gross margin",0.01,0.80,0.20)
st.json(price_recommendation(price,cost,margin))
st.warning("Price changes are proposals only and require authorized approval.")
