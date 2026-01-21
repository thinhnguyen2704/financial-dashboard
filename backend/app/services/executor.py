from typing import List
from app.services.execution import execute_trade
from app.schemas.backtest import BacktestRequest
from app.domain.models import Trade
from app.services.portfolio_factory import create_virtual_portfolio


class ExecutionResult:
    def __init__(self, equity_curve, trades):
        self.equity_curve = equity_curve
        self.trades = trades


def run_backtest(payload: BacktestRequest) -> ExecutionResult:
    portfolio = create_virtual_portfolio(payload.initial_cash)

    trades: List[Trade] = []
    equity_curve = []

    for t in payload.trades:
        trade = execute_trade(
            portfolio=portfolio,
            symbol=t.symbol,
            side=t.side,
            qty=float(t.quantity),
            price=float(t.price),
            fee=float(t.fee),
            slippage=float(t.slippage),
            timestamp=t.timestamp,
        )

        trades.append(trade)
        equity_curve.append(portfolio.cash)

    return ExecutionResult(equity_curve=equity_curve, trades=trades)
