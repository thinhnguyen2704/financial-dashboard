from decimal import Decimal
from app.domain.models import PortfolioState, Position as EnginePosition
from app.models.portfolio import Portfolio


def portfolio_to_state(portfolio: Portfolio) -> PortfolioState:
    return PortfolioState(
        cash=Decimal(portfolio.cash),
        positions={
            p.symbol: EnginePosition(
                symbol=p.symbol,
                quantity=Decimal(p.quantity),
                avg_price=Decimal(p.avg_price),
            )
            for p in portfolio.positions
        },
    )
