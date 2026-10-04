import streamlit as st
from app.services.approvals import create_proposal,approve
st.title("Automation & Approvals")
st.write("Recommendations and drafts remain human-controlled. Approval is bound to the exact material inputs and becomes invalid if they change.")
kind=st.selectbox("Workflow",["Scheduled forecast","Reorder alert","Purchase draft","Expiry review","Price proposal","Customer campaign","Finance summary","Market research"])
schedule=st.text_input("Schedule / trigger","Daily 08:00 store timezone"); payload=st.text_area("Proposed action / notes")
if st.button("Create proposal"):
    p=create_proposal(kind,{"notes":payload},{"kind":kind,"schedule":schedule,"notes":payload}); st.session_state.pending_proposal=p
p=st.session_state.get("pending_proposal")
if p:
    st.json(p)
    if st.button("Approve as demo owner"):
        try: st.session_state.pending_proposal=approve(p,"demo-owner",{"kind":kind,"schedule":schedule,"notes":payload}); st.success("Approved exact proposal.")
        except Exception as e: st.error(str(e))
st.caption("Production worker: durable Redis-backed Celery jobs with idempotency keys, bounded exponential retries, cancellation flags and PostgreSQL job/audit state.")
