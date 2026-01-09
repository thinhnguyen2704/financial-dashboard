import type { Trade } from "../types/trade";

export function connectTradeBlotter(
  portfolioId: number,
  token: string,
  onTrade: (trade: Trade) => void
) {
  const ws = new WebSocket(
    `ws://localhost:8000/ws/trades/${portfolioId}?token=${token}`
  );

  ws.onmessage = (e) => onTrade(JSON.parse(e.data));
  ws.onclose = () => console.log("Trade WS closed");

  return ws;
}
