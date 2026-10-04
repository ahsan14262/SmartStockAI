import pandas as pd, numpy as np
from app.analytics.forecasting import choose_forecast,rolling_origin_backtest,seasonal_naive,intermittent_croston

def test_forecast_selection_and_intervals():
    s=pd.Series(([10,12,9,11,13,8,7]*8),index=pd.date_range('2026-01-01',periods=56))
    name,pred,scores,intervals=choose_forecast(s,14)
    assert len(pred)==14 and len(intervals['lower_90'])==14
    assert any(isinstance(v,dict) and 'MAE' in v for v in scores.values())

def test_croston_nonnegative():
    s=pd.Series([0,0,3,0,0,0,2,0,0,4])
    assert np.all(intermittent_croston(s,5)>=0)
