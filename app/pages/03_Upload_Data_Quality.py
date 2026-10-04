import streamlit as st, pandas as pd, io
from app.services.ingestion import read_table,suggest_mapping,normalize,quality_report
from app.services.dataset_versions import persist_dataset
st.title("Upload & Data Quality")
st.caption("Upload → validate → map → clean → schema check → quality report → versioned storage → feature-ready dataset")
up=st.file_uploader("Sales file",type=["csv","tsv","xlsx","xls"])
if up:
    raw_bytes=up.getvalue(); raw=read_table(io.BytesIO(raw_bytes) if up.name.lower().endswith((".csv",".tsv")) else up)
    if not hasattr(raw,"columns"): st.error("Select one worksheet at a time in this MVP."); st.stop()
    st.subheader("Preview"); st.dataframe(raw.head(50),use_container_width=True)
    suggested=suggest_mapping(raw); mapping={}; st.subheader("Column mapping")
    for target in ["date","product_id","quantity","transaction_id","customer_id","price","cost","category","inventory_on_hand","lead_time_days"]:
        opts=[""]+list(raw.columns); default=opts.index(suggested[target]) if target in suggested else 0
        mapping[target]=st.selectbox(target,opts,index=default,key=target)
    st.info("Required for unit forecasting: date, product_id, quantity. Customer, margin, basket and replenishment features activate only when their real source fields exist.")
    if st.button("Validate, version & load",type="primary"):
        try:
            valid,rejected=normalize(raw,mapping); quality=quality_report(valid); manifest=persist_dataset(raw_bytes,up.name,valid,rejected,mapping,quality)
            st.session_state.sales_df=valid; st.session_state.dataset_manifest=manifest
            st.success(f"Loaded {len(valid)} valid rows; rejected {len(rejected)}. Dataset version: {manifest['version']}")
            st.json(quality)
            if len(rejected): st.download_button("Download rejected rows",rejected.to_csv(index=False),"rejected_rows.csv")
            st.download_button("Download corrected/validated data",valid.to_csv(index=False),"validated_sales.csv")
        except Exception as e: st.error(str(e))
else: st.caption("Try data/sample/sales.csv from the project.")
