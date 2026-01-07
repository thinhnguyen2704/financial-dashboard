from decimal import Decimal
from sqlalchemy.orm import Session

from app.domain.portfolio_engine import PortfolioEngine
from app.services.portfolio_state_mapper import portfolio_to_state
from app.models.portfolio import Portfolio


def compute_equity_snapshot(
    db: Session,
    portfolio_id: int,
    prices: dict[str, Decimal],
) -> dict:
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .one()
    )

    state = portfolio_to_state(portfolio)

    equity = PortfolioEngine.calculate_equity(state, prices)

    unrealized_pnl = equity - state.cash

    return {
        "portfolio_id": portfolio_id,
        "cash": state.cash,
        "equity": equity,
        "unrealized_pnl": unrealized_pnl,
        "positions": {
            symbol: {
                "quantity": pos.quantity,
                "avg_price": pos.avg_price,
                "mark_price": prices.get(symbol),
            }
            for symbol, pos in state.positions.items()
        },
    }
