import numpy as np

def sharpe(returns, risk_free=0.0):
    return np.mean(returns - risk_free) / np.std(returns)

def max_drawdown(equity_curve):
    peak = equity_curve[0]
    max_dd = 0
    for x in equity_curve:
        peak = max(peak, x)
        max_dd = min(max_dd, (x - peak) / peak)
    return max_dd
