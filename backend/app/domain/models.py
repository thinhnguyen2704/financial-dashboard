from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass(frozen=True)
class Trade:
    symbol: str
    side: str               # BUY or SELL
    quantity: Decimal
    price: Decimal
    fee: Decimal
    slippage: Decimal
    timestamp: datetime

@dataclass
class Position:
    symbol: str
    quantity: Decimal
    avg_price: Decimal

@dataclass
class PortfolioState:
    cash: Decimal
    positions: dict[str, Position]
