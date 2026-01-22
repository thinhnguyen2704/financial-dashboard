from app.services.execution import execute_trade
from app.services.portfolio_factory import VirtualPortfolioFactory
from app.schemas.backtest import TradeInput
from decimal import Decimal


class ExecutionResult:
    def __init__(self, portfolio, trades, equity_curve):
        self.portfolio = portfolio
        self.trades = trades
        self.equity_curve = equity_curve
        self.final_cash = portfolio.cash
        self.final_equity = portfolio.equity


def run_backtest(
    user_id: int,
    name: str,
    trades: list[TradeInput],
    initial_cash: Decimal,
) -> ExecutionResult:
    portfolio = VirtualPortfolioFactory.for_backtest(
        user_id=user_id,
        name=name,
        initial_cash=initial_cash,
    )

    executed_trades = []
    equity_curve = []

    for t in trades:
        trade = execute_trade(...)
        executed_trades.append(trade)
        equity_curve.append(portfolio.equity)

    return ExecutionResult(
        portfolio=portfolio,
        trades=executed_trades,
        equity_curve=equity_curve,
    )
