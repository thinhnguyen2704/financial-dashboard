from app.models.portfolio import Portfolio

def calculate_pnl(positions, prices: dict[str, float]):
    pnl = 0.0
    for pos in positions:
        current_price = prices.get(pos.symbol, pos.avg_price)
        pnl += (current_price - pos.avg_price) * pos.quantity
    return pnl

def calculate_equity(
    portfolio: Portfolio,
    prices: dict[str, float],
) -> float:
    """
    Total equity = cash + sum(position market value)
    """
    equity = portfolio.cash

    for position in portfolio.positions:
        price = prices.get(position.symbol)
        if price is None:
            continue

        equity += position.quantity * price

    return equity
