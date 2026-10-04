from pathlib import Path
import pandas as pd
import streamlit as st

from app.core.config import settings
from app.rag.chat import grounded_answer
from app.rag.store import HybridStore

st.title("Business Chatbot")
st.caption("Ask questions about your loaded sales data and indexed business knowledge.")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def get_sales_df():
    df = st.session_state.get("sales_df")
    if df is not None and not df.empty:
        return df, "loaded sales dataset"

    sample_path = Path("data/sample/sales.csv")
    if sample_path.exists():
        df = pd.read_csv(sample_path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        st.session_state.sales_df = df
        return df, "sample sales dataset"
    return None, None

def sales_evidence(df):
    evidence = []
    if df is None or df.empty:
        return evidence

    summary = [f"Sales dataset contains {len(df)} rows."]
    if "product_id" in df.columns:
        summary.append(f"It contains {df['product_id'].nunique()} unique products.")
    if "date" in df.columns:
        dates = pd.to_datetime(df["date"], errors="coerce").dropna()
        if not dates.empty:
            summary.append(f"Date range is {dates.min().date()} to {dates.max().date()}.")
    if {"price", "quantity"}.issubset(df.columns):
        revenue = (
            pd.to_numeric(df["price"], errors="coerce").fillna(0)
            * pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        ).sum()
        summary.append(f"Total revenue is {revenue:,.2f}.")
    evidence.append({"text": " ".join(summary), "metadata": {"source": "sales_summary"}})

    if {"product_id", "quantity"}.issubset(df.columns):
        work = df.copy()
        work["quantity"] = pd.to_numeric(work["quantity"], errors="coerce").fillna(0)
        grouped = work.groupby("product_id", as_index=False)["quantity"].sum()
        grouped = grouped.sort_values("quantity", ascending=False)
        text = "Product sales by total quantity: " + "; ".join(
            f"{row.product_id}: {row.quantity:g}" for row in grouped.head(20).itertuples()
        )
        evidence.append({"text": text, "metadata": {"source": "product_sales"}})

    if {"product_id", "inventory_on_hand"}.issubset(df.columns):
        work = df.copy()
        work["inventory_on_hand"] = pd.to_numeric(
            work["inventory_on_hand"], errors="coerce"
        )
        latest = work.dropna(subset=["inventory_on_hand"]).groupby("product_id").tail(1)
        text = "Latest inventory on hand: " + "; ".join(
            f"{row.product_id}: {row.inventory_on_hand:g}" for row in latest.itertuples()
        )
        evidence.append({"text": text, "metadata": {"source": "inventory"}})

    return evidence

def deterministic_answer(question, df):
    q = question.lower()
    if df is None or df.empty:
        return "No sales dataset is available yet. Load the sample dataset or upload sales data first."

    if "product_id" in df.columns and "quantity" in df.columns:
        work = df.copy()
        work["quantity"] = pd.to_numeric(work["quantity"], errors="coerce").fillna(0)
        totals = work.groupby("product_id")["quantity"].sum().sort_values(ascending=False)
        if any(word in q for word in ["top product", "best product", "most sold", "highest sales"]):
            return f"The top product by units sold is {totals.index[0]} with {totals.iloc[0]:g} units."

    if any(word in q for word in ["revenue", "sales amount", "total sales"]) and {"price", "quantity"}.issubset(df.columns):
        revenue = (
            pd.to_numeric(df["price"], errors="coerce").fillna(0)
            * pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        ).sum()
        return f"Total revenue in the loaded dataset is {revenue:,.2f}."

    if any(word in q for word in ["how many product", "number of product", "products"]):
        if "product_id" in df.columns:
            return f"The loaded dataset contains {df['product_id'].nunique()} unique products."

    return (
        "I can read the sales dataset, but AI generation is not configured. "
        "Try asking about total revenue, number of products, or the top product. "
        "For open-ended questions, configure GROQ_API_KEY in your Streamlit secrets/environment."
    )

q = st.chat_input("Ask about sales, products, inventory, revenue, or indexed knowledge")

if q:
    st.session_state.chat_messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.write(q)

    df, data_source = get_sales_df()
    evidence = sales_evidence(df)

    try:
        store = HybridStore(settings.default_tenant_id)
        indexed = store.search(q, 5)
        evidence.extend(indexed)
    except Exception:
        indexed = []

    try:
        if settings.groq_api_key and evidence:
            answer = grounded_answer(q, evidence)
        else:
            answer = deterministic_answer(q, df)
    except Exception as exc:
        answer = deterministic_answer(q, df)
        st.caption(f"AI provider unavailable; using local data fallback. ({type(exc).__name__})")

    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)

    with st.expander("Sources / context"):
        if data_source:
            st.write(f"Sales source: {data_source}")
        if indexed:
            st.write(f"Indexed knowledge results: {len(indexed)}")
        if not evidence:
            st.write("No business evidence is currently available.")
