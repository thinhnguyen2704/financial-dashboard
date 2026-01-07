# PCA-Stock Platform

A full‑stack quantitative trading and portfolio analytics platform with authenticated REST APIs, real‑time WebSocket streaming, and a React + TypeScript frontend.

---

## 1. Tech Stack

### Backend

* **FastAPI** (REST + WebSockets)
* **SQLAlchemy ORM**
* **PostgreSQL** (Dockerized)
* **JWT Authentication** (Access + Refresh tokens)
* **Role‑Based Access Control (RBAC)**
* **Passlib / bcrypt** for password hashing

### Frontend

* **React + TypeScript** (Vite)
* **AuthContext / AuthProvider**
* **Protected Routes**
* **JWT decoding & refresh logic**
* **WebSocket client with auto‑reconnect**
* **Charting for equity & PnL**

---

## 2. Core Features Implemented

### Authentication & Security

* User signup & login
* Password hashing (bcrypt)
* JWT access tokens
* Refresh tokens persisted in DB
* Token expiration handling
* Role‑based permissions (admin / user)
* Protected REST endpoints
* Authenticated WebSocket connections

### Database Models

* User
* RefreshToken
* Portfolio (structure prepared)

### WebSockets

* Authenticated equity / portfolio streaming
* JWT validation in WebSocket handshake
* Role‑based WebSocket access
* Auto‑disconnect handling

### Portfolio & Trading

* Portfolio state (cash, positions)
* Equity calculation pipeline
* PnL streaming (foundation)
* Transaction cost & slippage hooks

### Analytics

* Risk Metrics API

  * Sharpe Ratio
  * Max Drawdown
* Stateless batch computation
* Designed for backtests & live portfolios

---

## 3. API Overview

### Auth

* `POST /auth/signup`
* `POST /auth/login`
* `POST /auth/refresh`

### Risk

* `POST /risk/metrics`

### WebSockets

* `/ws/equity`
* `/ws/portfolio/{portfolio_id}`

---

## 4. Frontend Architecture

```
frontend/
├── auth/
│   ├── AuthContext.tsx
│   ├── AuthProvider.tsx
│   └── useAuth.ts
├── components/
│   ├── EquityChart.tsx
│   └── ProtectedRoute.tsx
├── pages/
│   ├── Login.tsx
│   ├── Signup.tsx
│   └── Dashboard.tsx
├── types/
│   ├── auth.ts
│   ├── portfolio.ts
│   └── risk.ts
└── services/
    ├── api.ts
    └── websocket.ts
```

---

## 5. Backend Architecture

```
backend/app/
├── api/routes/
│   ├── auth.py
│   ├── websocket.py
│   ├── risk.py
│   └── admin.py
├── core/
│   ├── security.py
│   ├── deps.py
│   └── deps_ws.py
├── db/
│   ├── base.py
│   ├── session.py
│   └── init_db.py
├── models/
│   ├── user.py
│   ├── refresh_token.py
│   └── portfolio.py
└── main.py
```

---

## 6. Current State

* Backend fully authenticated
* WebSocket auth stable
* Risk metrics API operational
* Frontend auth stable
* Portfolio streaming scaffolded

---

## 7. Known Non‑Issues (Resolved)

* bcrypt compatibility
* datetime / timezone bugs
* circular imports
* WebSocket JWT validation
* token expiration handling

---

# ROADMAP CHECKLIST

## Phase 1 — Portfolio Engine (NEXT)

* [ ] Persistent portfolio tables
* [ ] Position model
* [ ] Trade execution model
* [ ] Transaction costs & slippage
* [ ] Real equity calculation service

## Phase 2 — Strategy System

* [ ] Strategy configuration UI
* [ ] Signal → trade execution pipeline
* [ ] Backtesting engine
* [ ] Strategy result storage

## Phase 3 — Advanced Analytics

* [ ] Rolling Sharpe
* [ ] Sortino / Calmar
* [ ] Drawdown curves
* [ ] Risk metrics WebSocket stream

## Phase 4 — Market Data

* [ ] Intraday price ingestion
* [ ] Market data WebSocket
* [ ] Data normalization layer

## Phase 5 — Broker Integration

* [ ] Paper trading adapter
* [ ] Order lifecycle management
* [ ] Broker reconciliation

## Phase 6 — Deployment

* [ ] Docker Compose (API + DB + Frontend)
* [ ] Nginx reverse proxy
* [ ] Environment separation
* [ ] Production security hardening

---

## 8. Design Philosophy

* Stateless APIs
* Explicit security boundaries
* Deterministic calculations
* Frontend as pure consumer
* Backend as source of truth

---

## 9. Next Immediate Task

➡️ Implement **persistent portfolio & trade models** and connect them to live equity streaming.
