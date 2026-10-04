# Smart Stock Agent — implementation status

This repository implements a runnable reference/MVP covering the complete requested product surface. Features that require external credentials, production infrastructure, or measured business data are deliberately gated rather than faked.

## Implemented runnable capabilities
- Multipage Streamlit sitemap for all requested pages and six placeholder team profiles.
- CSV/TSV/XLS/XLSX ingestion, mapping, cleaning, rejected rows, quality reporting, raw preservation, version manifest and validated download.
- Canonical minimum forecasting schema (`date`, `product_id`, `quantity`) with optional fields activating downstream features.
- Daily/weekly demand series, seasonal naive, ETS, ARIMA and Croston intermittent baseline; rolling-origin evaluation; MAE/RMSE/sMAPE/WAPE/bias; measured selection; 90% approximate intervals; 7/14/30/90 horizons.
- EOQ, safety stock, ROP, inventory position and reorder recommendation scaffolding; approval-only action model.
- RFM, K-Means, leakage-aware churn label construction, FP-Growth basket rules with evidence thresholds.
- Pricing proposals with margin floors and human approval.
- FAISS + BM25 tenant/corpus/version storage, Groq-grounded chatbot scaffold and document extraction.
- DuckDuckGo/ddgs market research with evidence URLs, retrieval timestamps, assortment/stock distinction, trend evidence score and uncertain pilot scenarios.
- Multi-agent role definitions and short-path routing, reviewer role, bounded retry plan.
- Finance, HR/operations, reports (CSV/XLSX/DOCX/PDF), automation/approvals and admin pages.
- SQLAlchemy models, audit service, Docker/Compose, CI, security documentation and tests.

## Production-gated / extension capabilities
These cannot honestly be "completed" without credentials, measured datasets, or deployment choices: external IdP/MFA, live supplier/competitor APIs, email/SMS notifications, autonomous purchase/price execution, production Celery/Redis worker deployment, Chronos-2 benchmarking on the owner's hardware/data, multilingual retrieval benchmarking, OCR quality review workflow, and jurisdiction-specific legal compliance. The architecture leaves explicit integration points for them.

## Safety/product rule
No LLM is allowed to fabricate numerical forecasts, totals, inventory quantities, purchase execution, or live price changes. Exact values come from deterministic data/model tools; consequential actions remain approval-bound.
