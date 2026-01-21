from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.backtest import BacktestRequest
from app.services.executor import run_backtest

router = APIRouter(prefix="/backtests", tags=["Backtests"])


@router.post("/")
async def create_backtest(
    payload: BacktestRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Runs a backtest using the SAME execution pipeline as live trading.
    Persists trades, portfolio state, and equity history.
    """

    result = await run_backtest(
        db=db,
        user_id=user.id,
        name=payload.name,
        trades=payload.trades,
        price_provider=payload.price_provider,
        initial_cash=payload.initial_cash,
    )

    return {
        "backtest_id": result.backtest_id,
        "portfolio_id": result.portfolio_id,
        "equity_curve": result.equity_curve,
        "trades": [t.to_event_dict() for t in result.trades],
        "final_cash": result.final_cash,
        "final_equity": result.final_equity,
    }
