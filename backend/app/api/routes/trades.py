from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.portfolio import Portfolio
from app.domain.models import Trade
from app.services.trade_execution import execute_trade

router = APIRouter()


@router.post("/portfolios/{portfolio_id}/trades")
def place_trade(
    portfolio_id: int,
    trade: Trade,
    db: Session = Depends(get_db),
):
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .one()
    )

    state = execute_trade(db, portfolio, trade)

    db.commit()

    return {
        "cash": str(state.cash),
        "realized_pnl": str(state.realized_pnl),
    }
