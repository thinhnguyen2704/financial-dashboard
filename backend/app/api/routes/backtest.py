from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.backtest import BacktestRequest
from app.services.executor import run_backtest
from app.persistence.backtest_repository import persist_backtest

router = APIRouter(prefix="/backtests", tags=["Backtests"])


@router.post("/")
def create_backtest(
    payload: BacktestRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Runs a backtest using the SAME execution pipeline as live trading.
    Execution is pure; persistence is handled via adapter.
    """

    # 1. Execute (NO DB inside)
    execution = run_backtest(
        user_id=user.id,
        payload=payload,
    )

    # 2. Persist (DB boundary)
    backtest = persist_backtest(
        db=db,
        user_id=user.id,
        execution=execution,
    )

    # 3. Return API response
    return {
        "backtest_id": backtest.id,
        "portfolio_id": execution.portfolio.id,
        "equity_curve": execution.equity_curve,
        "trades": [t.to_event_dict() for t in execution.trades],
        "final_cash": execution.final_cash,
        "final_equity": execution.final_equity,
    }
