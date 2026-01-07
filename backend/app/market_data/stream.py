import json
import websockets
from decimal import Decimal
from app.market_data.cache import price_cache

ALPACA_WS = "wss://stream.data.alpaca.markets/v2/iex"

async def stream_prices(api_key: str, secret: str, symbols: list[str]):
    async with websockets.connect(ALPACA_WS) as ws:
        await ws.send(json.dumps({
            "action": "auth",
            "key": api_key,
            "secret": secret,
        }))

        await ws.send(json.dumps({
            "action": "subscribe",
            "trades": symbols,
        }))

        async for msg in ws:
            data = json.loads(msg)

            for event in data:
                if event["T"] == "t":  # trade
                    price_cache.update(
                        event["S"],
                        Decimal(str(event["p"]))
                    )
