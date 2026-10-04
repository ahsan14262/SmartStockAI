import streamlit as st, tempfile
from pathlib import Path
from app.rag.extract import extract_text,chunk_text
from app.rag.store import HybridStore
st.title("Settings & Administration")
st.subheader("Knowledge index")
docs=st.file_uploader("Add knowledge documents",type=["pdf","docx","txt","md"],accept_multiple_files=True)
if docs and st.button("Build isolated FAISS + BM25 index"):
    chunks=[]; meta=[]
    for d in docs:
        suffix=Path(d.name).suffix
        with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as f: f.write(d.getvalue()); p=f.name
        text=extract_text(p)
        for i,c in enumerate(chunk_text(text)):
            chunks.append(c); meta.append({"source":d.name,"chunk":i})
    HybridStore("demo-store").build(chunks,meta)
    st.success(f"Indexed {len(chunks)} chunks.")
st.subheader("Governance")
st.write("Production checklist: external IdP + MFA, server-side RBAC, tenant filters, secret manager, encrypted storage, safe upload scanning, audit retention, backups, incident process, prompt-injection tests, export authorization.")
