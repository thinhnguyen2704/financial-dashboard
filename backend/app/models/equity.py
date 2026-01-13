from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass(frozen=True)
class EquitySnapshot:
    timestamp: datetime
    equity: Decimal
    cash: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
