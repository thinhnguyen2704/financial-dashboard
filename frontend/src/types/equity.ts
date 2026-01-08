export interface EquityData {
	date: string;
	equity: number;
}

export interface EquityPosition {
	symbol: string;
	quantity: string;
	avg_price: string;
	market_price: string;
	unrealized_pnl: string;
}

export interface EquitySnapshot {
	timestamp: string;
	cash: string;
	equity: string;
  realized_pnl: string;
	unrealized_pnl: string;
	positions: EquityPosition[];
}
