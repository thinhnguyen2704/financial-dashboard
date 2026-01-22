from sqlalchemy.orm import Session
from app.models.backtest import Backtest, BacktestTrade, BacktestEquity
from app.services.executor import ExecutionResult


def persist_backtest(
    db: Session,
    *,
    user_id: int,
    execution: ExecutionResult,
) -> Backtest:
    backtest = Backtest(
        user_id=user_id,
        portfolio_id=execution.portfolio.id,
        final_cash=execution.final_cash,
        final_equity=execution.final_equity,
    )
    db.add(backtest)
    db.flush()

    for trade in execution.trades:
        db.add(
            BacktestTrade(
                backtest_id=backtest.id,
                **trade.to_event_dict(),
            )
        )

    for point in execution.equity_curve:
        db.add(
            BacktestEquity(
                backtest_id=backtest.id,
                timestamp=point.timestamp,
                equity=point.equity,
            )
        )

    db.commit()
    return backtest
