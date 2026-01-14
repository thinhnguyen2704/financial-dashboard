from sqlalchemy.orm import Session
from app.domain.portfolio_engine import PortfolioEngine
from app.services.portfolio_loader import get_or_create_runtime
from app.domain.models import Trade

async def execute_trade(
    db: Session,
    portfolio_id: int,
    trade: Trade
):
    runtime = get_or_create_runtime(db, portfolio_id)

    def apply(state):
        return PortfolioEngine.apply_trade(state, trade)

    return await runtime.apply(apply)
