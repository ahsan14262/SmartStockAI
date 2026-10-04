import streamlit as st, pandas as pd
from app.services.ingestion import read_table,suggest_mapping,normalize,quality_report
st.title("Upload & Data Quality")
up=st.file_uploader("Sales file",type=["csv","tsv","xlsx","xls"])
if up:
    raw=read_table(up); st.subheader("Preview"); st.dataframe(raw.head(50),use_container_width=True)
    suggested=suggest_mapping(raw)
    mapping={}
    st.subheader("Column mapping")
    for target in ["date","product_id","quantity","transaction_id","customer_id","price","cost","category","inventory_on_hand","lead_time_days"]:
        opts=[""]+list(raw.columns); default=opts.index(suggested[target]) if target in suggested else 0
        mapping[target]=st.selectbox(target,opts,index=default,key=target)
    if st.button("Validate & load"):
        try:
            valid,rejected=normalize(raw,mapping); st.session_state.sales_df=valid
            st.success(f"Loaded {len(valid)} valid rows; rejected {len(rejected)}.")
            st.json(quality_report(valid))
            if len(rejected): st.download_button("Download rejected rows",rejected.to_csv(index=False),"rejected_rows.csv")
        except Exception as e: st.error(str(e))
else:
    st.caption("Try data/sample/sales.csv from the downloadable project.")
