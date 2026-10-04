from datetime import datetime, timezone
from urllib.parse import urlparse

BLOCKED_QUERY_TERMS={"customer_id","employee","payroll","invoice number","email address","phone number"}

def safe_public_query(query: str) -> str:
    q=" ".join(str(query).split())[:300]
    if any(term in q.lower() for term in BLOCKED_QUERY_TERMS):
        raise ValueError("Public search query appears to contain confidential business/personal fields.")
    return q

def search_public(query,max_results=5,region="pk-en"):
    """DuckDuckGo-capable search via ddgs. Results are evidence, not verified sales."""
    from ddgs import DDGS
    q=safe_public_query(query)
    results=[]
    with DDGS() as ddgs:
        for r in ddgs.text(q, region=region, safesearch="moderate", max_results=max_results):
            url=r.get("href") or r.get("url")
            results.append({"title":r.get("title"),"url":url,"domain":urlparse(url).netloc if url else None,
                            "snippet":r.get("body"),"published_at":r.get("date"),
                            "retrieved_at":datetime.now(timezone.utc).isoformat()})
    return results
