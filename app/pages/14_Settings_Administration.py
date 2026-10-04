from pathlib import Path
import tempfile

import streamlit as st

from app.core.config import settings
from app.rag.extract import extract_text, chunk_text
from app.rag.store import HybridStore

st.title("Settings & Administration")

st.subheader("Knowledge Index")
st.write(
    "Upload business documents to create the private knowledge index used by the Business Chatbot."
)
st.caption("200MB per file • PDF, DOCX, TXT, MD")

index_dir = Path(settings.vectorstore_root) / settings.default_tenant_id / "business" / "v1"
manifest_path = index_dir / "manifest.json"

if manifest_path.exists():
    st.success("Knowledge index is available for the Business Chatbot.")
    try:
        st.json(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        pass
else:
    st.info("No knowledge index has been built yet. The chatbot can still answer from loaded sales data.")

docs = st.file_uploader(
    "Add knowledge documents",
    type=["pdf", "docx", "txt", "md"],
    accept_multiple_files=True,
)

if docs:
    st.write(f"{len(docs)} document(s) selected.")
    if st.button("Build FAISS + BM25 Knowledge Index", type="primary", use_container_width=True):
        chunks = []
        meta = []
        errors = []

        with st.spinner("Extracting documents and building the knowledge index..."):
            for d in docs:
                suffix = Path(d.name).suffix.lower()
                temp_path = None
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(d.getvalue())
                        temp_path = tmp.name

                    text = extract_text(temp_path)
                    document_chunks = chunk_text(text)
                    if not document_chunks:
                        errors.append(f"{d.name}: no extractable text")
                        continue

                    for i, chunk in enumerate(document_chunks):
                        chunks.append(chunk)
                        meta.append({"source": d.name, "chunk": i})
                except Exception as e:
                    errors.append(f"{d.name}: {e}")
                finally:
                    if temp_path:
                        try:
                            Path(temp_path).unlink(missing_ok=True)
                        except Exception:
                            pass

            if chunks:
                try:
                    HybridStore(settings.default_tenant_id).build(chunks, meta)
                    st.success(
                        f"Knowledge index built successfully: {len(chunks)} chunks "
                        f"from {len(docs)} selected document(s)."
                    )
                except Exception as e:
                    st.error(f"Could not build knowledge index: {e}")
            else:
                st.error("No usable text chunks were found in the selected documents.")

        for error in errors:
            st.warning(error)

st.divider()
st.subheader("AI Configuration")
if settings.groq_api_key:
    st.success(f"Groq is configured. Model: {settings.groq_model}")
else:
    st.warning(
        "GROQ_API_KEY is not configured. The Business Chatbot will use its local "
        "sales-data fallback, but open-ended AI answers require a Groq API key."
    )

st.caption(f"Tenant: {settings.default_tenant_id}")
st.caption(f"Embedding model: {settings.embedding_model}")

st.divider()
st.subheader("Governance")
st.write(
    "Production checklist: external IdP + MFA, server-side RBAC, tenant filters, "
    "secret manager, encrypted storage, safe upload scanning, audit retention, "
    "backups, incident process, prompt-injection tests, export authorization."
)
