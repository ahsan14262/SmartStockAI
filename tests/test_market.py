from app.analytics.market import catalog_status, score_evidence, analyze_opportunity

def test_not_carried_vs_out_of_stock():
    assert catalog_status("Protein Bars", ["Milk"], {}) == "NOT CARRIED"
    assert catalog_status("Milk", ["Milk"], {"Milk":0}) == "OUT OF STOCK"
    assert catalog_status("Milk", ["Milk"], {"Milk":3}) == "Available"

def test_opportunity_is_reviewable():
    ev=[{"title":"Protein bars growing trend","snippet":"popular demand trend","url":f"https://site{i}.example/a"} for i in range(5)]
    op=analyze_opportunity("Protein Bars",ev,[])
    assert 0 <= op.trend_score <= 100
    assert "CONSIDER" in op.recommendation or "MONITOR" in op.recommendation
