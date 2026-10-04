from pathlib import Path
import streamlit as st
import pandas as pd

from app.services.ingestion import read_table, suggest_mapping, normalize, quality_report
from app.services.dataset_versions import persist_dataset

st.title("Upload & Data Quality")
st.caption("Upload → validate → map → clean → schema check → quality report → versioned storage → feature-ready dataset")
st.caption("200MB per file • CSV, TSV, XLSX, XLS")

sample_path = Path("data/sample/sales.csv")

if st.button("🧪 Load Sample Dataset", use_container_width=True):
    try:
        if not sample_path.exists():
            st.error("Sample dataset not found at data/sample/sales.csv")
        else:
            raw_bytes = sample_path.read_bytes()
            raw = pd.read_csv(sample_path)
            suggested = suggest_mapping(raw)
            mapping = {
                target: suggested.get(target, "")
                for target in [
                    "date", "product_id", "quantity", "transaction_id",
                    "customer_id", "price", "cost", "category",
                    "inventory_on_hand", "lead_time_days"
                ]
            }
            valid, rejected = normalize(raw, mapping)
            quality = quality_report(valid)
            manifest = persist_dataset(
                raw_bytes, sample_path.name, valid, rejected, mapping, quality
            )
            st.session_state.sales_df = valid
            st.session_state.dataset_manifest = manifest
            st.session_state.sample_loaded = True
            st.success(
                f"Sample dataset loaded: {len(valid)} valid rows; "
                f"{len(rejected)} rejected. Dataset version: {manifest['version']}"
            )
    except Exception as e:
        st.error(f"Could not load sample dataset: {e}")

if st.session_state.get("sample_loaded") and st.session_state.get("sales_df") is not None:
    sample_df = st.session_state.sales_df
    st.subheader("Loaded Sample Preview")
    st.dataframe(sample_df.head(50), use_container_width=True)

st.divider()
st.subheader("Upload Your Dataset")

up = st.file_uploader("Sales file", type=["csv", "tsv", "xlsx", "xls"])

if up:
    try:
        raw_bytes = up.getvalue()
        up.seek(0)
        raw = read_table(up)
    except Exception as e:
        st.error(f"Could not read uploaded file: {e}")
        st.stop()

    if not hasattr(raw, "columns"):
        st.error("Select one worksheet at a time in this MVP.")
        st.stop()

    st.subheader("Preview")
    st.dataframe(raw.head(50), use_container_width=True)

    suggested = suggest_mapping(raw)
    mapping = {}
    st.subheader("Column mapping")

    targets = [
        "date", "product_id", "quantity", "transaction_id", "customer_id",
        "price", "cost", "category", "inventory_on_hand", "lead_time_days"
    ]

    for target in targets:
        opts = [""] + list(raw.columns)
        default = opts.index(suggested[target]) if target in suggested and suggested[target] in opts else 0
        mapping[target] = st.selectbox(target, opts, index=default, key=f"mapping_{target}")

    st.info(
        "Required for unit forecasting: date, product_id, quantity. "
        "Customer, margin, basket and replenishment features activate only "
        "when their real source fields exist."
    )

    if st.button("Validate, version & load", type="primary"):
        try:
            valid, rejected = normalize(raw, mapping)
            quality = quality_report(valid)
            manifest = persist_dataset(
                raw_bytes, up.name, valid, rejected, mapping, quality
            )
            st.session_state.sales_df = valid
            st.session_state.dataset_manifest = manifest
            st.session_state.sample_loaded = False

            st.success(
                f"Loaded {len(valid)} valid rows; rejected {len(rejected)}. "
                f"Dataset version: {manifest['version']}"
            )
            st.json(quality)

            if len(rejected):
                st.download_button(
                    "Download rejected rows",
                    rejected.to_csv(index=False),
                    "rejected_rows.csv",
                )

            st.download_button(
                "Download corrected/validated data",
                valid.to_csv(index=False),
                "validated_sales.csv",
            )
        except Exception as e:
            st.error(str(e))
else:
    st.caption("Or upload your own file above. For a quick demo, use Load Sample Dataset.")
