class PortfolioError(Exception):
    pass

class InsufficientCash(PortfolioError):
    pass

class InvalidTrade(PortfolioError):
    pass

class PositionViolation(PortfolioError):
    pass
