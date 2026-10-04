import math
from statistics import NormalDist
def eoq(annual_demand, ordering_cost, holding_cost_per_unit):
    if min(annual_demand,ordering_cost,holding_cost_per_unit)<=0: return 0.0
    return math.sqrt((2*annual_demand*ordering_cost)/holding_cost_per_unit)
def safety_stock(daily_std, lead_time_days, service_level=0.95):
    z=NormalDist().inv_cdf(service_level)
    return max(0.0,z*daily_std*math.sqrt(max(lead_time_days,0)))
def reorder_point(avg_daily_demand, lead_time_days, safety):
    return max(0.0,avg_daily_demand*lead_time_days+safety)
def inventory_position(on_hand,on_order=0,reserved=0,backorders=0):
    return on_hand+on_order-reserved-backorders
def reorder_qty(target_stock, position, pack_size=1):
    need=max(0,target_stock-position)
    return math.ceil(need/max(pack_size,1))*max(pack_size,1)
def days_of_cover(on_hand,avg_daily_demand):
    return float("inf") if avg_daily_demand<=0 else on_hand/avg_daily_demand
