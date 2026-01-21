from app.domain.models import Trade
from datetime import datetime
from decimal import Decimal


# Atomic execution of a trade with slippage and fee calculation
def execute_trade(
    portfolio,
    symbol: str,
    side: str,
    qty: float,
    market_price: float,
    timestamp: datetime | None = None,
):
    slippage = market_price * 0.0005
    fee = max(1.0, qty * market_price * 0.001)

    execution_price = (
        market_price + slippage if side == "BUY" else market_price - slippage
    )
    cost = execution_price * qty + fee

    if side == "BUY" and portfolio.cash < cost:
        raise ValueError("Insufficient cash")

    portfolio.cash -= cost if side == "BUY" else -cost

    trade = Trade(
        timestamp=timestamp or datetime.utcnow(),
        symbol=symbol,
        side=side,
        quantity=Decimal(str(qty)),
        price=Decimal(str(execution_price)),
        fee=Decimal(str(fee)),
        slippage=Decimal(str(slippage)),
    )

    return trade
