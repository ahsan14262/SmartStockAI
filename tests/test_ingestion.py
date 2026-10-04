import pandas as pd
from app.services.ingestion import normalize
def test_normalize():
    df=pd.DataFrame({"Date":["2026-01-01"],"SKU":["A"],"Qty":[2]})
    valid,rejected=normalize(df,{"date":"Date","product_id":"SKU","quantity":"Qty"})
    assert len(valid)==1 and len(rejected)==0
