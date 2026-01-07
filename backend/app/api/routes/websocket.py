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
from app.services.pnl import calculate_equity
from app.services.market_data import get_latest_prices
from app.services.portfolio import load_portfolio

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
async def portfolio_stream(ws: WebSocket, portfolio_id: int):
    user = await get_current_user_ws(ws)
    await ws.accept()

    db = SessionLocal()

    try:
        portfolio = load_portfolio(portfolio_id, user)
        symbols = [p.symbol for p in portfolio.positions]

        while True:
            prices = await get_latest_prices(symbols)
            equity = calculate_equity(portfolio, prices)

            await ws.send_json(
                {
                    "equity": equity,
                    "cash": portfolio.cash,
                    "positions": [
                        {
                            "symbol": p.symbol,
                            "qty": p.quantity,
                            "price": prices.get(p.symbol),
                        }
                        for p in portfolio.positions
                    ],
                }
            )

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass
    finally:
        db.close()
