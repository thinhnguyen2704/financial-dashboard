from fastapi import FastAPI
from app.api.routes import auth, backtest, websocket
from app.core.config import settings

print("DATABASE_URL:", settings.DATABASE_URL)

app = FastAPI(title="Trading Platform API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(backtest.router, prefix="/backtest", tags=["backtest"])
app.include_router(websocket.router)
