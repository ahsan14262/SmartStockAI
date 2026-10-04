AGENTS={
"orchestrator":{"goal":"Route requests to the minimum required tools/agents.","permissions":["routing","read_authorized_context"]},
"market_research":{"goal":"Research public product/price evidence with citations.","permissions":["public_search","catalog_read"]},
"sales_customer":{"goal":"Support retention, segmentation and baskets.","permissions":["sales_read","customer_analytics"]},
"forecasting":{"goal":"Produce measured forecasts using deterministic tools.","permissions":["sales_read","forecast_run"]},
"inventory":{"goal":"Prepare replenishment and expiry proposals.","permissions":["inventory_read","purchase_draft"]},
"finance":{"goal":"Evaluate margins, budgets and cash scenarios.","permissions":["finance_read"]},
"hr":{"goal":"Support schedules and approved policy Q&A.","permissions":["hr_restricted_read"]},
"writer":{"goal":"Organize verified outputs into reports.","permissions":["report_write"]},
"reviewer":{"goal":"Check evidence, arithmetic, citations, completeness and permissions.","permissions":["review"]},
}
