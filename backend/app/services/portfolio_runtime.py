import asyncio
from app.domain.models import PortfolioState

class PortfolioRuntime:
    def __init__(self, state: PortfolioState):
        self.state = state
        self.lock = asyncio.Lock()

    async def apply(self, fn):
        async with self.lock:
            self.state = fn(self.state)
            return self.state
