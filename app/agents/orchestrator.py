from app.agents.definitions import AGENTS
def route(query):
    q=query.lower()
    if any(x in q for x in ["forecast","demand","next week"]): return ["forecasting","inventory","reviewer"]
    if any(x in q for x in ["customer","churn","basket","rfm"]): return ["sales_customer","reviewer"]
    if any(x in q for x in ["market","competitor","trend"]): return ["market_research","reviewer"]
    if any(x in q for x in ["cash","margin","finance"]): return ["finance","reviewer"]
    return ["orchestrator","reviewer"]
def plan(query): return {"query":query,"route":route(query),"status":"planned","bounded_retries":2}
