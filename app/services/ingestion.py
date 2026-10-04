import pandas as pd, hashlib, io
CANONICAL = ["date","product_id","quantity","transaction_id","customer_id","price","cost","category","inventory_on_hand","lead_time_days"]
ALIASES={
 "date":["date","timestamp","sale_date","datetime"],
 "product_id":["product_id","sku","product","item_id"],
 "quantity":["quantity","qty","units","units_sold"],
 "transaction_id":["transaction_id","invoice","invoice_id","order_id"],
 "customer_id":["customer_id","customer","customer_code"],
 "price":["price","unit_price","selling_price"],
 "cost":["cost","unit_cost","purchase_price"],
 "category":["category","product_category"],
 "inventory_on_hand":["inventory_on_hand","stock","on_hand"],
 "lead_time_days":["lead_time_days","lead_time"],
}
def read_table(upload):
    name=upload.name.lower()
    if name.endswith(".csv"): return pd.read_csv(upload)
    if name.endswith(".tsv"): return pd.read_csv(upload,sep="\t")
    if name.endswith((".xlsx",".xls")): return pd.read_excel(upload)
    raise ValueError("Supported structured formats: CSV, TSV, XLSX, XLS.")
def suggest_mapping(df):
    low={str(c).lower().strip():c for c in df.columns}; out={}
    for target,names in ALIASES.items():
        for n in names:
            if n in low: out[target]=low[n]; break
    return out
def normalize(df,mapping):
    inv={src:target for target,src in mapping.items() if src}
    x=df.rename(columns=inv).copy()
    missing=[c for c in ["date","product_id","quantity"] if c not in x.columns]
    if missing: raise ValueError("Missing required mapped fields: "+", ".join(missing))
    x["date"]=pd.to_datetime(x["date"],errors="coerce")
    x["product_id"]=x["product_id"].astype(str).str.strip()
    x["quantity"]=pd.to_numeric(x["quantity"],errors="coerce")
    rejected=x[x[["date","product_id","quantity"]].isna().any(axis=1)].copy()
    valid=x.drop(rejected.index).drop_duplicates().copy()
    return valid,rejected
def quality_report(df):
    return {"rows":len(df),"columns":len(df.columns),"duplicate_rows":int(df.duplicated().sum()),
            "missing_cells":int(df.isna().sum().sum()),"date_min":str(df["date"].min()) if "date" in df else None,
            "date_max":str(df["date"].max()) if "date" in df else None}
def checksum_bytes(data): return hashlib.sha256(data).hexdigest()
