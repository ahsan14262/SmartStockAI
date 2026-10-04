import streamlit as st
st.title("About Us")
st.write("Smart Stock Agent is designed for a six-member delivery team.")
for i in range(1,7):
    st.subheader(f"Team Member {i}")
    st.caption("Role • Photo • Biography • Contact — replace with approved team information.")
