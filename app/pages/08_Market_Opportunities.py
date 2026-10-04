import streamlit as st
import pandas as pd
from app.integrations.market_search import search_public
from app.analytics.market import analyze_opportunity

st.title("🌐 Market Analyzer")
st.write("Research public market signals, compare them with your assortment, and surface reviewable product opportunities.")

df=st.session_state.get("sales_df")
catalog=[]; stock={}
if df is not None and "product_id" in df:
    catalog=df["product_id"].dropna().astype(str).unique().tolist()
    if "inventory_on_hand" in df:
        stock=(df.dropna(subset=["inventory_on_hand"]).groupby(df["product_id"].astype(str))["inventory_on_hand"].last().to_dict())

c1,c2=st.columns([2,1])
with c1: products=st.text_input("Products to investigate (comma-separated)","protein bars, almond milk, organic oats")
with c2: region=st.selectbox("Search region",["pk-en","us-en","wt-wt"],index=0)
context=st.text_input("Market context","Pakistan grocery retail trends and prices")

if st.button("Search Market Trends",type="primary"):
    rows=[]; detailed=[]
    for product in [p.strip() for p in products.split(",") if p.strip()][:8]:
        try:
            evidence=search_public(f'"{product}" {context}',max_results=5,region=region)
            op=analyze_opportunity(product,evidence,catalog,stock)
            detailed.append(op)
            rows.append({"Product":op.product,"Trend Score":f"{op.trend_score}/100","Current Stock":op.current_stock,
                         "Recommendation":op.recommendation,"Evidence":op.evidence_count,"Confidence":op.confidence})
        except Exception as e:
            rows.append({"Product":product,"Trend Score":"N/A","Current Stock":"Unknown","Recommendation":"Search unavailable","Evidence":0,"Confidence":"none"})
            st.warning(f"{product}: {e}")
    if rows:
        st.subheader("🔥 Trending Opportunities")
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        for op in detailed:
            with st.expander(f"{op.product} — {op.recommendation}"):
                st.write(op.rationale)
                if op.pilot_quantity: st.info(f"Uncertain pilot scenario: {op.pilot_quantity} units. Confirm supplier MOQ, margin, shelf life and budget before approval.")
                for e in op.evidence:
                    st.markdown(f"**{e.get('title') or 'Source'}**  \n{e.get('snippet') or ''}  \n{e.get('url') or ''}  \nRetrieved: {e.get('retrieved_at')}")

st.caption("Trend Score is an internal evidence score, not verified sales or search volume. 'Best-selling' must be supported by market- and period-specific evidence. No purchase is executed automatically.")
