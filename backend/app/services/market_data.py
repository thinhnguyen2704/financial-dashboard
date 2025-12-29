import asyncio
from fastapi import WebSocket

async def stream_prices(ws: WebSocket):
    while True:
        await ws.send_json({
            "symbol": "AAPL",
            "price": 187.23
        })
        await asyncio.sleep(1)
