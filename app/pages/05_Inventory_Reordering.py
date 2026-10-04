import streamlit as st
from app.analytics.inventory import eoq,safety_stock,reorder_point,inventory_position,reorder_qty
st.title("Inventory & Reordering")
avg=st.number_input("Average daily demand",0.0,value=10.0); std=st.number_input("Daily demand std. dev.",0.0,value=3.0)
lead=st.number_input("Lead time (days)",0.0,value=5.0); on=st.number_input("On hand",0.0,value=30.0)
on_order=st.number_input("On order",0.0,value=0.0); reserved=st.number_input("Reserved",0.0,value=0.0)
annual=avg*365; order_cost=st.number_input("Ordering cost",0.01,value=500.0); hold=st.number_input("Annual holding cost/unit",0.01,value=100.0)
ss=safety_stock(std,lead,.95); rop=reorder_point(avg,lead,ss); pos=inventory_position(on,on_order,reserved,0)
st.metric("EOQ",f"{eoq(annual,order_cost,hold):.1f}"); st.metric("Safety stock",f"{ss:.1f}"); st.metric("ROP",f"{rop:.1f}")
st.metric("Inventory position",f"{pos:.1f}"); st.metric("Suggested order",f"{reorder_qty(rop+avg*7,pos):.0f}")
st.caption("Recommendation only. Purchasing requires approval.")
