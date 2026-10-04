import streamlit as st, pandas as pd
from app.analytics.forecasting import prepare_series,choose_forecast
st.title("Demand Forecasting")
df=st.session_state.get("sales_df")
if df is None: st.info("Upload sales data first."); st.stop()
sku=st.selectbox("Product",sorted(df.product_id.astype(str).unique())); freq=st.selectbox("Frequency",["D","W"],format_func=lambda x:"Daily" if x=="D" else "Weekly")
h=st.selectbox("Horizon",[7,14,30,90]); series=prepare_series(df,sku,freq)
st.caption("Models are selected from measured chronological backtests; the chatbot must use these numerical outputs rather than invent forecasts.")
if st.button("Run rolling-origin model selection",type="primary"):
    name,pred,scores,intervals=choose_forecast(series,h); future=pd.date_range(series.index.max()+pd.tseries.frequencies.to_offset(freq),periods=h,freq=freq)
    out=pd.DataFrame({"date":future,"forecast_quantity":pred,"lower_90":intervals["lower_90"],"upper_90":intervals["upper_90"]})
    st.session_state.latest_forecast={"product_id":sku,"model":name,"rows":out.to_dict("records"),"dataset_version":st.session_state.get("dataset_manifest",{}).get("version")}
    st.success(f"Selected: {name}"); st.dataframe(pd.DataFrame(scores).T,use_container_width=True); st.line_chart(out.set_index("date")[["forecast_quantity","lower_90","upper_90"]]); st.dataframe(out,use_container_width=True)
