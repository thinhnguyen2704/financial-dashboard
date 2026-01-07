from decimal import Decimal
from threading import Lock

class PriceCache:
    def __init__(self):
        self._prices: dict[str, Decimal] = {}
        self._lock = Lock()

    def update(self, symbol: str, price: Decimal):
        with self._lock:
            self._prices[symbol] = price

    def get(self, symbol: str) -> Decimal | None:
        return self._prices.get(symbol)


price_cache = PriceCache()
