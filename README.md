# Smart Stock Agent

A modular retail decision-support application for general stores. This generated codebase is a new,
standalone implementation based on the Smart Stock Agent specification. It does not modify the
existing ChatGPT Project/workspace.

## Included
- Streamlit multipage UI
- Authentication demo + RBAC scaffolding
- SQLAlchemy database layer (SQLite local default; PostgreSQL via `DATABASE_URL`)
- CSV/XLSX/XLS/TSV ingestion and validation
- Forecasting baselines: seasonal naive, Exponential Smoothing, ARIMA, optional Prophet
- Inventory: EOQ, ROP, safety stock, days of cover
- Customer analytics: RFM, K-Means, churn baseline, market basket
- RAG: extraction, chunking, FAISS semantic index, BM25 keyword search, reciprocal-rank fusion,
  optional cross-encoder reranking, citations
- Groq-backed grounded chatbot with deterministic fallback
- CrewAI-compatible agent definitions plus deterministic orchestration fallback
- Market research integration scaffold
- Reports/exports: CSV/XLSX/DOCX/PDF
- Audit logging, approvals, jobs, tests, Docker, CI

## Quick start
1. Install Python 3.11.
2. Create a virtual environment.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`.
5. `streamlit run app.py`

Demo credentials:
- owner@example.com / ChangeMe123!
- manager@example.com / ChangeMe123!

Change demo credentials before any real deployment.

## PostgreSQL
Set `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/smartstock`.
SQLite is used only as a convenient local default.

## Optional AI services
Set `GROQ_API_KEY` for LLM answers. RAG and analytics still work without it.
Heavy models are loaded lazily and are not required for the basic demo.

## Important
This is an implementation starter suitable for development and demonstration, not a claim of
production readiness or business/forecast accuracy. Validate models on your own data, configure a
real identity provider, harden deployment, and complete security/release testing before production.
