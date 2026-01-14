from collections import defaultdict
from typing import Dict
from app.services.portfolio_runtime import PortfolioRuntime

portfolio_runtimes: Dict[int, PortfolioRuntime] = {}

# symbol → set[portfolio_id]
portfolios_by_symbol: dict[str, set[int]] = defaultdict(set)


def register_portfolio_symbols(portfolio_id: int, symbols: list[str]):
    for s in symbols:
        portfolios_by_symbol[s].add(portfolio_id)


def unregister_portfolio_symbols(portfolio_id: int):
    for s in list(portfolios_by_symbol.keys()):
        portfolios_by_symbol[s].discard(portfolio_id)


def unregister_portfolio_runtime(portfolio_id: int):
    portfolio_runtimes.pop(portfolio_id, None)
 