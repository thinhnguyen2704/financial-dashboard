from sqlalchemy.orm import Session

from app.domain.portfolio_engine import PortfolioEngine
from app.domain.models import Trade as EngineTrade
from app.services.portfolio_state_mapper import portfolio_to_state
from app.services.portfolio_persistence import persist_state
from app.models.trade import Trade
from app.models.portfolio import Portfolio


def execute_trade(
    db: Session,
    portfolio: Portfolio,
    trade: EngineTrade,
):
    state = portfolio_to_state(portfolio)
    new_state = PortfolioEngine.apply_trade(state, trade)

    db.add(
        Trade(
            portfolio_id=portfolio.id,
            symbol=trade.symbol,
            side=trade.side,
            quantity=trade.quantity,
            price=trade.price,
            fee=trade.fee,
            slippage=trade.slippage,
            timestamp=trade.timestamp,
        )
    )

    persist_state(db, portfolio, new_state)
