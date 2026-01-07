from app.models.portfolio import Portfolio

def execute_trade(
    portfolio: Portfolio,
    symbol: str,
    side: str,
    qty: float,
    market_price: float,
):
    slippage = market_price * 0.0005
    fee = max(1.0, qty * market_price * 0.001)

    execution_price = market_price + slippage if side == "BUY" else market_price - slippage
    cost = execution_price * qty + fee

    if side == "BUY" and portfolio.cash < cost:
        raise ValueError("Insufficient cash")

    portfolio.cash -= cost if side == "BUY" else -cost

    return execution_price, fee, slippage
