"""Deterministic market-opportunity scoring built on public-search evidence.
Search evidence is a signal, never proof of sales volume.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable
import re

POSITIVE_TERMS = ("trend", "popular", "demand", "growing", "new", "launch", "seasonal", "bestseller", "best-selling")
RISK_TERMS = ("recall", "shortage", "warning", "ban", "expired", "unsafe")

@dataclass
class MarketOpportunity:
    product: str
    trend_score: int
    evidence_count: int
    current_stock: str
    recommendation: str
    pilot_quantity: int | None
    confidence: str
    rationale: str
    evidence: list[dict]

    def to_dict(self): return asdict(self)

def _norm(v: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(v).lower()).strip()

def catalog_status(product: str, catalog: Iterable[str], stock_by_product: dict[str, float] | None = None) -> str:
    target=_norm(product)
    matches=[x for x in catalog if target == _norm(x) or target in _norm(x) or _norm(x) in target]
    if not matches: return "NOT CARRIED"
    if stock_by_product:
        qty=max(float(stock_by_product.get(str(x), stock_by_product.get(_norm(x), 0)) or 0) for x in matches)
        return "Available" if qty > 0 else "OUT OF STOCK"
    return "Carried (stock unknown)"

def score_evidence(product: str, evidence: list[dict]) -> int:
    """Transparent 0-100 evidence score; deliberately not called a sales score."""
    if not evidence: return 0
    product_tokens=set(_norm(product).split())
    score=35
    domains=set()
    for row in evidence[:8]:
        text=_norm(f"{row.get('title','')} {row.get('snippet','')}")
        overlap=len(product_tokens & set(text.split())) / max(1,len(product_tokens))
        score += round(7*overlap)
        score += min(4, sum(1 for t in POSITIVE_TERMS if t in text))
        score -= min(8, 3*sum(1 for t in RISK_TERMS if t in text))
        url=str(row.get('url',''))
        if '//' in url: domains.add(url.split('/')[2].lower())
    score += min(12, len(domains)*3)
    return max(0,min(100,int(score)))

def analyze_opportunity(product: str, evidence: list[dict], catalog: Iterable[str], stock_by_product: dict[str,float] | None=None) -> MarketOpportunity:
    status=catalog_status(product,catalog,stock_by_product)
    score=score_evidence(product,evidence)
    confidence="low" if len(evidence)<2 else "medium" if len(evidence)<5 else "higher"
    if status == "NOT CARRIED" and score >= 65:
        rec="🟢 CONSIDER ADDING TO STOCK"
        pilot=5 if score < 80 else 10
        rationale="Public evidence suggests an opportunity, but there is no store sales history. Start with a small reviewable pilot."
    elif status == "OUT OF STOCK" and score >= 60:
        rec="🟠 REVIEW REPLENISHMENT"
        pilot=None
        rationale="The product is already carried but currently out of stock; use internal demand forecasts before choosing quantity."
    elif status.startswith("Available") and score >= 70:
        rec="🟠 CONSIDER INCREASING STOCK"
        pilot=None
        rationale="External evidence is positive; validate against forecast, margin, shelf life and supplier constraints."
    else:
        rec="⚪ MONITOR / NO ACTION"
        pilot=None
        rationale="Evidence is not strong enough for an inventory action."
    return MarketOpportunity(product,score,len(evidence),status,rec,pilot,confidence,rationale,evidence)
