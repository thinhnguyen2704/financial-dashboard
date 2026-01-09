from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.portfolio import Portfolio
from app.domain.models import Trade
from app.services.trade_execution import execute_trade
from app.api.websockets.manager import trade_ws_manager

router = APIRouter()


@router.post("/portfolios/{portfolio_id}/trades")
async def place_trade(
    portfolio_id: int,
    trade: Trade,
    db: Session = Depends(get_db),
):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).one()

    state = execute_trade(db, portfolio, trade)

    db.commit()
    await trade_ws_manager.broadcast(
        portfolio_id=trade.portfolio_id,
        payload=trade.to_event_dict(),
    )

    return {
        "cash": str(state.cash),
        "realized_pnl": str(state.realized_pnl),
    }
