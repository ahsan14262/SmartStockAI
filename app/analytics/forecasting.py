import pandas as pd, numpy as np

def prepare_series(df, product_id, freq="D"):
    x=df[df.product_id.astype(str)==str(product_id)].copy()
    return x.groupby(pd.Grouper(key="date",freq=freq))["quantity"].sum().asfreq(freq,fill_value=0).astype(float)

def seasonal_naive(series,horizon,season=7):
    vals=series.values; base=vals[-season:] if len(vals)>=season else vals
    return np.zeros(horizon) if len(base)==0 else np.resize(base,horizon)

def exponential_smoothing(series,horizon,season=7):
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    seasonal="add" if len(series)>=season*2 else None
    model=ExponentialSmoothing(series,trend="add" if len(series)>=4 else None,seasonal=seasonal,seasonal_periods=season if seasonal else None).fit(optimized=True)
    return np.maximum(0,model.forecast(horizon).values)

def arima(series,horizon):
    from statsmodels.tsa.arima.model import ARIMA
    return np.maximum(0,ARIMA(series,order=(1,1,1)).fit().forecast(horizon).values)

def intermittent_croston(series,horizon,alpha=.1):
    y=np.asarray(series,float); nz=np.flatnonzero(y>0)
    if not len(nz): return np.zeros(horizon)
    z=y[nz[0]]; p=max(1,nz[0]+1); last=nz[0]
    for i in nz[1:]:
        z=alpha*y[i]+(1-alpha)*z; interval=i-last; p=alpha*interval+(1-alpha)*p; last=i
    return np.full(horizon,max(0,z/max(p,1e-9)))

def _metrics(actual,pred):
    a=np.asarray(actual,float); p=np.asarray(pred,float); err=a-p
    mae=float(np.mean(np.abs(err))); rmse=float(np.sqrt(np.mean(err**2)))
    denom=np.abs(a)+np.abs(p); smape=float(np.mean(np.where(denom==0,0,2*np.abs(err)/denom))*100)
    bias=float(np.mean(p-a)); wape=float(np.sum(np.abs(err))/max(np.sum(np.abs(a)),1e-9)*100)
    return {"MAE":mae,"RMSE":rmse,"sMAPE_pct":smape,"WAPE_pct":wape,"bias":bias}

def rolling_origin_backtest(series, method, horizon=7, folds=3):
    min_train=max(14,horizon*2); results=[]
    for fold in range(folds,0,-1):
        end=len(series)-(fold-1)*horizon
        start_test=end-horizon
        if start_test<min_train: continue
        train=series.iloc[:start_test]; test=series.iloc[start_test:end]
        pred=method(train,len(test)); results.append(_metrics(test.values,pred))
    if not results: return None
    return {k:float(np.mean([r[k] for r in results])) for k in results[0]} | {"folds":len(results)}

def candidate_methods(series):
    methods={"Seasonal naive":lambda s,h:seasonal_naive(s,h,7),"Exponential smoothing":lambda s,h:exponential_smoothing(s,h,7),"ARIMA":arima}
    zero_rate=float((series==0).mean()) if len(series) else 0
    if zero_rate>=.35: methods["Croston intermittent"]=intermittent_croston
    return methods

def choose_forecast(series,horizon=7):
    methods=candidate_methods(series); scores={}
    for name,fn in methods.items():
        try: scores[name]=rolling_origin_backtest(series,fn,min(7,horizon),3)
        except Exception as e: scores[name]={"error":str(e)}
    valid={k:v for k,v in scores.items() if isinstance(v,dict) and "MAE" in v and np.isfinite(v["MAE"])}
    winner=min(valid,key=lambda k:(valid[k]["MAE"],abs(valid[k]["bias"]))) if valid else "Seasonal naive"
    pred=methods[winner](series,horizon)
    residual_scale=(valid.get(winner) or {}).get("RMSE",float(np.std(series.values[-30:])) if len(series) else 0)
    lower=np.maximum(0,pred-1.64*residual_scale); upper=np.maximum(lower,pred+1.64*residual_scale)
    return winner,pred,scores,{"lower_90":lower,"upper_90":upper,"selection_metric":"rolling-origin MAE"}
