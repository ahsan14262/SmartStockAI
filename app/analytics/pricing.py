def price_recommendation(current_price, unit_cost, target_margin=.20, max_change=.10):
    floor=unit_cost/(1-target_margin) if target_margin<1 else current_price
    lo=max(floor,current_price*(1-max_change)); hi=current_price*(1+max_change)
    return {"floor":round(floor,2),"allowed_min":round(lo,2),"allowed_max":round(hi,2),
            "status":"proposal_requires_approval"}
