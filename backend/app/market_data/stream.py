import json
import websockets
from decimal import Decimal
from app.market_data.cache import price_cache
from app.services.equity_throttle import equity_throttle
from app.services.portfolio_registry import portfolios_by_symbol


ALPACA_WS = "wss://stream.data.alpaca.markets/v2/iex"


async def stream_prices(api_key: str, secret: str, symbols: list[str]):
    async with websockets.connect(ALPACA_WS) as ws:
        await ws.send(
            json.dumps(
                {
                    "action": "auth",
                    "key": api_key,
                    "secret": secret,
                }
            )
        )

        await ws.send(
            json.dumps(
                {
                    "action": "subscribe",
                    "trades": symbols,
                }
            )
        )

        async for msg in ws:
            data = json.loads(msg)

            for event in data:
                if event["T"] == "t":  # trade
                    price_cache.update(event["S"], Decimal(str(event["p"])))

                for portfolio_id in portfolios_by_symbol.get(event["S"], []):
                    await equity_throttle.trigger(portfolio_id)
