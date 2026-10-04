import streamlit as st
from app.core.auth import login,logout,current_user
st.title("Sign In & Onboarding")
u=current_user()
if u:
    st.success(f"Signed in as {u['name']} ({u['role']})")
    if st.button("Sign out"): logout(); st.rerun()
else:
    email=st.text_input("Email",value="owner@example.com")
    password=st.text_input("Password",type="password",value="ChangeMe123!")
    if st.button("Sign in"):
        if login(email,password): st.success("Signed in."); st.rerun()
        else: st.error("Invalid credentials.")
st.warning("Demo authentication is for local development. Configure a supported external identity provider before production.")
