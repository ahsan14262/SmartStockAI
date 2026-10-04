from app.analytics.inventory import eoq,safety_stock,reorder_point,inventory_position
def test_eoq_positive(): assert eoq(1000,50,2)>0
def test_rop(): assert reorder_point(10,5,20)==70
def test_position(): assert inventory_position(100,20,10,5)==105
def test_safety_stock_nonnegative(): assert safety_stock(3,5,.95)>=0
