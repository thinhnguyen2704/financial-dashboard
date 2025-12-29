from fastapi import WebSocket, APIRouter
from app.core.deps_ws import get_current_user_ws
from app.services.market_data import stream_prices
from app.core.deps_ws import get_current_user_ws as authenticate_ws

router = APIRouter()


@router.websocket("/ws/equity")
async def equity_stream(ws: WebSocket):
    await ws.accept()

    await get_current_user_ws(ws)

    while True:
        await ws.send_json({"equity": 100000})


@router.websocket("/ws/prices")
async def prices(ws: WebSocket):
    await authenticate_ws(ws)
    await stream_prices(ws)
