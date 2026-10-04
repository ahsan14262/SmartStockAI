import pandas as pd, numpy as np
def rfm(df):
    req={"customer_id","date","transaction_id","price","quantity"}
    if not req.issubset(df.columns): raise ValueError("RFM needs customer_id, date, transaction_id, price and quantity.")
    x=df.dropna(subset=["customer_id"]).copy()
    x["amount"]=x["price"]*x["quantity"]
    snap=x["date"].max()+pd.Timedelta(days=1)
    out=x.groupby("customer_id").agg(
        recency=("date",lambda s:(snap-s.max()).days),
        frequency=("transaction_id","nunique"),
        monetary=("amount","sum")).reset_index()
    return out
def kmeans_segments(rfm_df,k=4):
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    cols=["recency","frequency","monetary"]
    z=StandardScaler().fit_transform(np.log1p(rfm_df[cols]))
    out=rfm_df.copy()
    out["segment"]=KMeans(n_clusters=min(k,len(out)),random_state=42,n_init="auto").fit_predict(z)
    return out
def basket_rules(df,min_support=.02):
    if not {"transaction_id","product_id"}.issubset(df.columns): raise ValueError("Basket analysis needs transaction_id and product_id.")
    from mlxtend.frequent_patterns import fpgrowth, association_rules
    basket=(df.assign(v=1).pivot_table(index="transaction_id",columns="product_id",values="v",aggfunc="max",fill_value=0)>0)
    itemsets=fpgrowth(basket,min_support=min_support,use_colnames=True)
    return association_rules(itemsets,metric="lift",min_threshold=1.0) if len(itemsets) else pd.DataFrame()
