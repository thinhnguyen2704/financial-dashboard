from decimal import Decimal
from sqlalchemy.orm import Session

from app.domain.portfolio_engine import PortfolioEngine
from app.domain.models import PortfolioState, Trade as DomainTrade
from app.models.portfolio import Portfolio
from app.models.trade import Trade as TradeORM


def rebuild_portfolio_state(
    db: Session,
    portfolio_id: int,
) -> PortfolioState:
    """
    Rebuild portfolio state by replaying trades in chronological order.
    This is deterministic and idempotent.
    """

    portfolio: Portfolio | None = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .first()
    )

    if portfolio is None:
        raise ValueError(f"Portfolio {portfolio_id} not found")

    # Initial state
    state = PortfolioState(
        cash=Decimal(str(portfolio.initial_cash)),
        positions={},
        realized_pnl=Decimal("0"),
    )

    trades: list[TradeORM] = (
        db.query(TradeORM)
        .filter(TradeORM.portfolio_id == portfolio_id)
        .order_by(TradeORM.timestamp.asc())
        .all()
    )

    for t in trades:
        domain_trade = DomainTrade(
            trade_id=t.id,
            symbol=t.symbol,
            side=t.side,
            quantity=Decimal(str(t.quantity)),
            price=Decimal(str(t.price)),
            fee=Decimal(str(t.fee or 0)),
            slippage=Decimal(str(t.slippage or 0)),
            timestamp=t.timestamp,
        )

        state = PortfolioEngine.apply_trade(state, domain_trade)

    return state
