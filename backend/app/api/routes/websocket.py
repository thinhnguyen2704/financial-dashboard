from fastapi import WebSocket, APIRouter
from app.core.deps_ws import get_current_user_ws
from app.services.market_data import stream_prices
from app.core.deps_ws import get_current_user_ws as authenticate_ws
from app.models.role import Role
import asyncio

router = APIRouter()


@router.websocket("/ws/equity")
async def equity_stream(ws: WebSocket):
    await ws.accept()
    user = await get_current_user_ws(ws, required_role=Role.user)

    while True:
        await ws.send_json(
            {
                "equity": 100000,
                "user": user.email,
            }
        )
        await asyncio.sleep(1)


@router.websocket("/ws/admin/metrics")
async def admin_metrics(ws: WebSocket):
    await ws.accept()
    admin = await get_current_user_ws(ws, required_role=Role.admin)

    while True:
        await ws.send_json(
            {
                "active_users": 42,
                "uptime": "99.99%",
            }
        )
        await asyncio.sleep(2)



@router.websocket("/ws/prices")
async def prices(ws: WebSocket):
    await authenticate_ws(ws)
    await stream_prices(ws)
