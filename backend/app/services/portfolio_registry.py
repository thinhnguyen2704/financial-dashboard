from collections import defaultdict

# symbol → set[portfolio_id]
portfolios_by_symbol: dict[str, set[int]] = defaultdict(set)


def register_portfolio(portfolio_id: int, symbols: list[str]):
    for s in symbols:
        portfolios_by_symbol[s].add(portfolio_id)


def unregister_portfolio(portfolio_id: int):
    for s in list(portfolios_by_symbol.keys()):
        portfolios_by_symbol[s].discard(portfolio_id)
