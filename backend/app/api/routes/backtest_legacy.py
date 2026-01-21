from fastapi import APIRouter, Depends
import yfinance as yf
from app.core.security import get_current_user
from app.services.backtesting import backtest

router = APIRouter()


@router.post("/")
def run_backtest(ticker: str, user: str = Depends(get_current_user)):
    df = yf.download(ticker)
    df["Returns"] = df["Close"].pct_change()
    df["signal"] = (df["Close"] > df["Close"].rolling(20).mean()).astype(int)

    result = backtest(df)

    return {"equity": result["equity"].dropna().to_dict()}
