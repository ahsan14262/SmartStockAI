import streamlit as st
from app.rag.store import HybridStore
from app.rag.chat import grounded_answer
st.title("Business Chatbot")
q=st.chat_input("Ask about your indexed business knowledge")
if q:
    with st.chat_message("user"): st.write(q)
    try:
        store=HybridStore("demo-store"); evidence=store.search(q,5)
        ans=grounded_answer(q,evidence)
        with st.chat_message("assistant"): st.write(ans)
        with st.expander("Sources"):
            for i,e in enumerate(evidence): st.write(f"S{i+1}: {e['metadata']}")
    except Exception:
        st.info("No knowledge index yet. Build one from Settings & Administration.")
