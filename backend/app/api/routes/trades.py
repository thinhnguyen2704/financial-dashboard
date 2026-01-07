from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.portfolio import Portfolio
from app.domain.models import Trade as EngineTrade
from backend.app.services.trade_execution import execute_trade
from app.schemas.trade import TradeCreate

router = APIRouter(prefix="/portfolios", tags=["trades"])


@router.post("/{portfolio_id}/trades")
def place_trade(
    portfolio_id: int,
    trade_in: TradeCreate,
    db: Session = Depends(get_db),
):
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .with_for_update()
        .one_or_none()
    )

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    trade = EngineTrade(
        symbol=trade_in.symbol,
        side=trade_in.side,
        quantity=trade_in.quantity,
        price=trade_in.price,
        fee=trade_in.fee,
        slippage=trade_in.slippage,
        timestamp=trade_in.timestamp,
    )

    try:
        execute_trade(db, portfolio, trade)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "executed"}
