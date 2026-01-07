from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class TradeCreate(BaseModel):
    symbol: str
    side: str
    quantity: Decimal
    price: Decimal
    fee: Decimal = Decimal("0")
    slippage: Decimal = Decimal("0")
    timestamp: datetime
