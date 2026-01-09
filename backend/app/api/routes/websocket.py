from fastapi import WebSocket, APIRouter
from app.core.deps_ws import get_current_user_ws
from app.services.market_data import stream_prices
from app.core.deps_ws import get_current_user_ws as authenticate_ws
from app.models.role import Role
from app.db.session import SessionLocal
from app.models.portfolio import Portfolio
from app.services.pnl import calculate_pnl
from starlette.websockets import WebSocketDisconnect
import asyncio
from app.api.websockets.manager import trade_ws_manager
from app.services.portfolio_registry import (
    register_portfolio,
    unregister_portfolio,
    get_portfolio_symbols,
)
from app.db.session import SessionLocal

router = APIRouter()


@router.websocket("/ws/equity")
async def equity_stream(ws: WebSocket):
    await ws.accept()
    try:
        await get_current_user_ws(ws, required_role=Role.user)
    except RuntimeError as e:
        reason = str(e)

        if reason == "TOKEN_EXPIRED":
            await ws.close(code=4001, reason=reason)
        elif reason == "Forbidden":
            await ws.close(code=4003, reason=reason)
        else:
            await ws.close(code=4000, reason=reason)
        return

    try:
        while True:
            await ws.send_json({"equity": 100_000})
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        # Client disconnected — clean exit
        print("WebSocket disconnected")

    except Exception as e:
        # Unexpected error — log & close
        print("WebSocket error:", e)
        await ws.close()


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


@router.websocket("/ws/portfolio/{portfolio_id}")
async def portfolio_ws(ws: WebSocket, portfolio_id: int):
    await get_current_user_ws(ws)

    # Register socket
    await trade_ws_manager.connect(portfolio_id, ws)

    # Register portfolio → symbols
    db = SessionLocal()
    try:
        symbols = get_portfolio_symbols(db, portfolio_id)
        register_portfolio(portfolio_id, symbols)
    finally:
        db.close()

    try:
        while True:
            await ws.receive_text()  # keep-alive
    except WebSocketDisconnect:
        pass
    finally:
        # CLEANUP IS HERE
        unregister_portfolio(portfolio_id)
        trade_ws_manager.disconnect(portfolio_id, ws)
