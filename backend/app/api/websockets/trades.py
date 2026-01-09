from fastapi import WebSocket, Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.websockets.manager import trade_ws_manager
from app.core.deps_ws import get_current_user_ws
from app.db.session import get_db
from app.models.trade import Trade

router = APIRouter()


@router.websocket("/ws/trades/{portfolio_id}")
async def trades_ws(
    websocket: WebSocket,
    portfolio_id: int,
    user=Depends(get_current_user_ws),
    db: Session = Depends(get_db),
):
    # Authorization
    portfolio = (
        db.query(Trade.portfolio).filter(Trade.portfolio_id == portfolio_id).first()
    )

    if not portfolio or (portfolio.user_id != user.id and not user.is_admin):
        await websocket.close(code=1008)
        return

    await trade_ws_manager.connect(portfolio_id, websocket)

    # Replay last N trades
    trades = (
        db.query(Trade)
        .filter(Trade.portfolio_id == portfolio_id)
        .order_by(Trade.timestamp.desc())
        .limit(50)
        .all()
    )

    for t in reversed(trades):
        await websocket.send_json(t.to_event_dict())

    try:
        while True:
            await websocket.receive_text()  # keep alive
    finally:
        trade_ws_manager.disconnect(portfolio_id, websocket)
