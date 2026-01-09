from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TradeEvent:
    trade_id: int
    portfolio_id: int
    symbol: str
    side: str
    quantity: Decimal
    price: Decimal
    fee: Decimal
    slippage: Decimal
    realized_pnl: Decimal
    timestamp: datetime
