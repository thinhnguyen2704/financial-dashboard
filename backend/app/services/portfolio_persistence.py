from app.models.position import Position
from app.models.portfolio import Portfolio
from app.domain.models import PortfolioState


def persist_state(db, portfolio: Portfolio, state: PortfolioState):
    portfolio.cash = state.cash

    existing = {p.symbol: p for p in portfolio.positions}

    for symbol, pos in state.positions.items():
        if symbol in existing:
            existing[symbol].quantity = pos.quantity
            existing[symbol].avg_price = pos.avg_price
        else:
            db.add(
                Position(
                    portfolio_id=portfolio.id,
                    symbol=symbol,
                    quantity=pos.quantity,
                    avg_price=pos.avg_price,
                )
            )

    for symbol in set(existing) - set(state.positions):
        db.delete(existing[symbol])
