def calculate_pnl(positions, prices: dict[str, float]):
    pnl = 0.0
    for pos in positions:
        current_price = prices.get(pos.symbol, pos.avg_price)
        pnl += (current_price - pos.avg_price) * pos.quantity
    return pnl
