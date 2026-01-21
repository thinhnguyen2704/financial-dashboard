from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import List, Literal


class TradeInput(BaseModel):
    timestamp: datetime
    symbol: str
    side: Literal["BUY", "SELL"]

    quantity: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)

    fee: Decimal = Decimal("0")
    slippage: Decimal = Decimal("0")


class BacktestRequest(BaseModel):
    name: str
    initial_cash: Decimal = Field(..., gt=0)
    trades: List[TradeInput]
