from decimal import Decimal
from app.domain.models import PortfolioState, Position as DomainPosition
from app.models.portfolio import Portfolio
from app.models.position import Position as DBPosition


def load_state_from_db(portfolio: Portfolio) -> PortfolioState:
    positions = {
        p.symbol: DomainPosition(
            symbol=p.symbol,
            quantity=Decimal(p.quantity),
            avg_price=Decimal(p.avg_price),
        )
        for p in portfolio.positions
    }

    return PortfolioState(
        cash=Decimal(portfolio.cash),
        positions=positions,
        realized_pnl=Decimal(portfolio.realized_pnl),
    )


def persist_state_to_db(portfolio: Portfolio, state: PortfolioState, session):
    portfolio.cash = state.cash
    portfolio.realized_pnl = state.realized_pnl

    portfolio.positions.clear()

    for pos in state.positions.values():
        portfolio.positions.append(
            DBPosition(
                symbol=pos.symbol,
                quantity=pos.quantity,
                avg_price=pos.avg_price,
            )
        )

    session.add(portfolio)
