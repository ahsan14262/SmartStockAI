import pandas as pd, numpy as np

def rfm(df):
    req={"customer_id","date","transaction_id","price","quantity"}
    if not req.issubset(df.columns): raise ValueError("RFM needs customer_id, date, transaction_id, price and quantity.")
    x=df.dropna(subset=["customer_id"]).copy(); x["amount"]=pd.to_numeric(x["price"],errors="coerce")*x["quantity"]
    snap=x["date"].max()+pd.Timedelta(days=1)
    return x.groupby("customer_id").agg(recency=("date",lambda s:(snap-s.max()).days),frequency=("transaction_id","nunique"),monetary=("amount","sum")).reset_index()

def kmeans_segments(rfm_df,k=4):
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    if len(rfm_df)<2: raise ValueError("Segmentation needs at least two customers.")
    cols=["recency","frequency","monetary"]; z=StandardScaler().fit_transform(np.log1p(rfm_df[cols].clip(lower=0)))
    out=rfm_df.copy(); out["segment"]=KMeans(n_clusters=min(k,len(out)),random_state=42,n_init=10).fit_predict(z); return out

def churn_labels(df,inactivity_days=60,prediction_horizon_days=30):
    if not {"customer_id","date"}.issubset(df.columns): raise ValueError("Churn needs customer_id and date.")
    x=df.dropna(subset=["customer_id"]).copy(); cutoff=x.date.max()-pd.Timedelta(days=prediction_horizon_days)
    hist=x[x.date<=cutoff]; future=x[x.date>cutoff]
    last=hist.groupby("customer_id").date.max(); future_ids=set(future.customer_id.astype(str))
    out=pd.DataFrame({"customer_id":last.index.astype(str),"days_since_purchase":(cutoff-last).dt.days.values})
    out["churned"]=((out.days_since_purchase>=inactivity_days)&(~out.customer_id.isin(future_ids))).astype(int)
    return out,{"observation_end":str(cutoff),"prediction_horizon_days":prediction_horizon_days,"inactivity_days":inactivity_days}

def basket_rules(df,min_support=.02,min_confidence=.2):
    if not {"transaction_id","product_id"}.issubset(df.columns): raise ValueError("Basket analysis needs transaction_id and product_id.")
    from mlxtend.frequent_patterns import fpgrowth, association_rules
    x=df.dropna(subset=["transaction_id","product_id"]); basket=(x.assign(v=1).pivot_table(index="transaction_id",columns="product_id",values="v",aggfunc="max",fill_value=0)>0)
    if len(basket)<10: raise ValueError("Basket analysis needs at least 10 transactions for a minimally useful result.")
    itemsets=fpgrowth(basket,min_support=min_support,use_colnames=True)
    rules=association_rules(itemsets,metric="confidence",min_threshold=min_confidence) if len(itemsets) else pd.DataFrame()
    return rules.sort_values(["lift","confidence"],ascending=False) if len(rules) else rules
