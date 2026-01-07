from fastapi import WebSocket
from typing import Dict
import random
import asyncio


async def stream_prices(ws: WebSocket):
    while True:
        await ws.send_json({"symbol": "AAPL", "price": 187.23})
        await asyncio.sleep(1)


async def get_latest_prices(symbols: list[str]) -> Dict[str, float]:
    """
    Temporary market data provider.
    Replace later with live feed (Polygon, IB, etc.)
    """
    return {symbol: random.uniform(90, 110) for symbol in symbols}
