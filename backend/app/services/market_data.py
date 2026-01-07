from fastapi import WebSocket
from typing import Dict
import asyncio
from decimal import Decimal


async def stream_prices(ws: WebSocket):
    while True:
        await ws.send_json({"symbol": "AAPL", "price": 187.23})
        await asyncio.sleep(1)


async def get_latest_prices(symbols: list[str]) -> Dict[str, float]:
    """
    Temporary market data provider.
    Replace later with live feed (Polygon, IB, etc.)
    """
    return {symbol: Decimal("100") for symbol in symbols}