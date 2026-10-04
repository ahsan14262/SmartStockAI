import streamlit as st
from app.core.security import hash_password, verify_password
USERS = {
 "owner@example.com":{"password":hash_password("ChangeMe123!"),"role":"owner","name":"Demo Owner"},
 "manager@example.com":{"password":hash_password("ChangeMe123!"),"role":"manager","name":"Demo Manager"},
}
def login(email,password):
    u=USERS.get(email.lower())
    if u and verify_password(password,u["password"]):
        st.session_state.user={"email":email.lower(),"role":u["role"],"name":u["name"],"tenant_id":"demo-store"}
        return True
    return False
def logout(): st.session_state.pop("user",None)
def current_user(): return st.session_state.get("user")
