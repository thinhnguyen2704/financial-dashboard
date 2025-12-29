from fastapi import APIRouter, WebSocket
import asyncio
import random

router = APIRouter()

@router.websocket("/ws/equity")
async def equity_stream(ws: WebSocket):
    await ws.accept()
    equity = 10000

    try:
        while True:
            equity *= 1 + random.uniform(-0.001, 0.001)
            await ws.send_json({
                "equity": equity
            })
            await asyncio.sleep(1)
    except Exception:
        await ws.close()
