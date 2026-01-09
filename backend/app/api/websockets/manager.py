from collections import defaultdict
from fastapi import WebSocket
from typing import Dict, Set

# One manager per event type
# Portfolio-scoped
# No global fan-out mistakes


class TradeWebSocketManager:
    def __init__(self):
        self.connections: Dict[int, Set[WebSocket]] = defaultdict(set)

    async def connect(self, portfolio_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[portfolio_id].add(websocket)

    def disconnect(self, portfolio_id: int, websocket: WebSocket):
        self.connections[portfolio_id].discard(websocket)

    async def broadcast(self, portfolio_id: int, payload: dict):
        for ws in list(self.connections[portfolio_id]):
            await ws.send_json(payload)


trade_ws_manager = TradeWebSocketManager()
