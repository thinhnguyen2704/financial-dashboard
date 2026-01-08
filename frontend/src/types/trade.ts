export interface Trade {
  timestamp: string;
  symbol: string;
  side: "BUY" | "SELL";
  quantity: string;
  price: string;
  fee: string;
  realized_pnl: string;
}
