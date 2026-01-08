from decimal import Decimal
from dataclasses import dataclass, field

@dataclass
class PortfolioState:
    cash: Decimal
    positions: dict
    realized_pnl: Decimal = Decimal("0")
