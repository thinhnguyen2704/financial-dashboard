from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import auth, backtest, websocket, admin
from app.db.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware
import app.models  # noqa: F401
from app.db import base  # noqa
from app.api.routes import risk, equity_ws

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (optional cleanup)


app = FastAPI(title="Trading Platform API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(backtest.router, prefix="/backtest", tags=["backtest"])
app.include_router(websocket.router)
app.include_router(risk.router)
app.include_router(admin.router)
app.include_router(equity_ws.router)
