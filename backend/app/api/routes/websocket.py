from fastapi import WebSocket, APIRouter
from app.core.deps_ws import get_current_user_ws
from app.services.market_data import stream_prices
from app.core.deps_ws import get_current_user_ws as authenticate_ws
from app.models.role import Role
from app.db.session import SessionLocal
from app.models.portfolio import Portfolio
from app.services.pnl import calculate_pnl
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
    await get_current_user_ws(ws, required_role=Role.admin)

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


@router.websocket("/ws/pnl")
async def pnl_stream(ws: WebSocket):
    await ws.accept()
    user = await get_current_user_ws(ws)

    db = SessionLocal()
    try:
        portfolio = db.query(Portfolio).filter(Portfolio.owner_id == user.id).first()

        while True:
            prices = {
                "AAPL": 190.0,
                "MSFT": 410.0,
            }

            pnl = calculate_pnl(portfolio.positions, prices)

            await ws.send_json(
                {
                    "portfolio": portfolio.name,
                    "pnl": pnl,
                }
            )

            await asyncio.sleep(1)
    finally:
        db.close()
