import pandas as pd, numpy as np
def prepare_series(df, product_id, freq="D"):
    x=df[df.product_id.astype(str)==str(product_id)].copy()
    x=x.groupby(pd.Grouper(key="date",freq=freq))["quantity"].sum().asfreq(freq,fill_value=0)
    return x.astype(float)
def seasonal_naive(series,horizon,season=7):
    vals=series.values
    base=vals[-season:] if len(vals)>=season else vals
    if len(base)==0: return np.zeros(horizon)
    return np.resize(base,horizon)
def exponential_smoothing(series,horizon,season=7):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    seasonal="add" if len(series)>=season*2 else None
    sp=season if seasonal else None
    model=ExponentialSmoothing(series,trend="add" if len(series)>=4 else None,seasonal=seasonal,seasonal_periods=sp).fit(optimized=True)
    return np.maximum(0,model.forecast(horizon).values)
def arima(series,horizon):
    from statsmodels.tsa.arima.model import ARIMA
    model=ARIMA(series,order=(1,1,1)).fit()
    return np.maximum(0,model.forecast(horizon).values)
def backtest_mae(series, method, horizon=7):
    if len(series)<max(21,horizon*2): return None
    train,test=series.iloc[:-horizon],series.iloc[-horizon:]
    pred=method(train,horizon)
    return float(np.mean(np.abs(test.values-pred)))
def choose_forecast(series,horizon=7):
    candidates={"Seasonal naive":lambda s,h:seasonal_naive(s,h,7),
                "Exponential smoothing":lambda s,h:exponential_smoothing(s,h,7),
                "ARIMA":lambda s,h:arima(s,h)}
    scores={}
    for name,fn in candidates.items():
        try: scores[name]=backtest_mae(series,fn,min(7,horizon))
        except Exception: scores[name]=None
    valid={k:v for k,v in scores.items() if v is not None and np.isfinite(v)}
    winner=min(valid,key=valid.get) if valid else "Seasonal naive"
    return winner,candidates[winner](series,horizon),scores
