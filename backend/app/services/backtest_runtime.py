from app.services.portfolio_runtime import PortfolioRuntime
from app.domain.models import PortfolioState


def create_backtest_runtime(initial_cash):
    state = PortfolioState(
        cash=initial_cash,
        positions={},
        realized_pnl=0,
    )
    return PortfolioRuntime(state)
