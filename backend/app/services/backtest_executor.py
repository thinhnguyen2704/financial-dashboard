from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.portfolio_engine import PortfolioEngine
from app.services.backtest_runtime import create_backtest_runtime
from app.models.backtest import Backtest
from app.models.backtest_run import BacktestRun
from app.domain.models import Trade
from app.schemas.backtest import TradeInput


def to_domain_trade(t: TradeInput) -> Trade:
    return Trade(
        timestamp=t.timestamp,
        symbol=t.symbol,
        side=t.side,
        quantity=t.quantity,
        price=t.price,
        fee=t.fee,
        slippage=t.slippage,
    )


async def run_backtest(
    db: Session,
    user_id: int,
    name: str,
    trades: list,
    price_provider,
    initial_cash: Decimal,
):
    runtime = create_backtest_runtime(initial_cash)

    equity_series = []

    for trade in trades:
        async with runtime.lock:
            runtime.state = PortfolioEngine.apply_trade(runtime.state, trade)

            prices = price_provider(trade.timestamp)
            equity = PortfolioEngine.calculate_equity(runtime.state, prices)

        equity_series.append(
            BacktestRun(
                timestamp=trade.timestamp,
                equity=float(equity),
            )
        )

    backtest = Backtest(
        user_id=user_id,
        name=name,
        start_date=equity_series[0].timestamp,
        end_date=equity_series[-1].timestamp,
        initial_cash=float(initial_cash),
        final_equity=equity_series[-1].equity,
        runs=equity_series,
    )

    db.add(backtest)
    db.commit()
    db.refresh(backtest)

    return backtest
