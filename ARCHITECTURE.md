# Architecture

UI (Streamlit multipage) → authenticated application services → SQLAlchemy transactional store.
Analytics are deterministic Python services. RAG uses tenant/corpus/version-isolated FAISS plus BM25,
with reciprocal-rank fusion and source metadata. Exact totals should come from SQL/calculation tools,
not approximate retrieval. Groq is optional and receives only the minimum authorized context.
Agent routing is bounded and tool-based; consequential purchase/price/HR actions require approval.

## Production upgrades
Replace demo auth with an external OIDC identity provider; enforce authorization at every service and
query boundary. Add Alembic migrations, durable object storage, Redis + a durable worker, malware
scanning, KMS/secret manager, observability, backup/restore drills, rate limits and CSRF/SSRF/path
traversal controls. Add tenant_id constraints/indexes to every tenant-owned table and integration test
cross-tenant denial.

## Forecasting
Benchmark seasonal naive, ETS/Holt-Winters, ARIMA/SARIMA, Prophet, intermittent-demand methods,
lag-feature ML and a Hugging Face time-series model (e.g. Chronos family) using rolling-origin
validation. Select by measured performance, latency and hardware—not by model reputation.

## Agent flow
Authorization → retrieval/research → deterministic analysis/calculation → verification → writing →
independent review → final report. Simple questions take a short path.
