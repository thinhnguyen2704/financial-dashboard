import asyncio
from decimal import Decimal

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.equity import compute_equity_snapshot
from app.core.deps_ws import get_current_user_ws
from app.models.portfolio import Portfolio


router = APIRouter()


@router.websocket("/ws/equity/{portfolio_id}")
async def equity_stream(
    websocket: WebSocket,
    portfolio_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_ws),
):
    await websocket.accept()

    try:
        while True:
            portfolio = (
                db.query(Portfolio)
                .filter(Portfolio.id == portfolio_id)
                .one()
            )

            symbols = {pos.symbol for pos in portfolio.positions}

            # Phase 1 stub pricing
            prices = {symbol: Decimal("100") for symbol in symbols}

            snapshot = compute_equity_snapshot(
                db=db,
                portfolio_id=portfolio_id,
                prices=prices,
            )

            await websocket.send_json(snapshot)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass
