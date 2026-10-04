import streamlit as st
st.title("HR & Operations")
st.info("HR support is intentionally scoped: scheduling, onboarding drafts and approved policy Q&A. Consequential employment decisions remain human-controlled.")
name=st.text_input("Employee / shift label"); availability=st.text_area("Availability / constraints")
if st.button("Prepare staffing draft"): st.write({"label":name,"constraints":availability,"status":"draft_requires_manager_review"})
