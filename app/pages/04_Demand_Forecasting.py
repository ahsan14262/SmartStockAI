import streamlit as st, pandas as pd
from app.analytics.forecasting import prepare_series,choose_forecast
st.title("Demand Forecasting")
df=st.session_state.get("sales_df")
if df is None: st.info("Upload sales data first."); st.stop()
sku=st.selectbox("Product",sorted(df.product_id.astype(str).unique()))
h=st.selectbox("Horizon",[7,14,30,90])
series=prepare_series(df,sku)
if st.button("Run measured model selection"):
    name,pred,scores=choose_forecast(series,h)
    future=pd.date_range(series.index.max()+pd.Timedelta(days=1),periods=h)
    out=pd.DataFrame({"date":future,"forecast_quantity":pred})
    st.success(f"Selected: {name}"); st.json(scores); st.line_chart(out.set_index("date")); st.dataframe(out)
