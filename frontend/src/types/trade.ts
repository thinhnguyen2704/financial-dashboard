export interface Trade {
	trade_id: number;
	portfolio_id: number;
	symbol: string;
	side: 'BUY' | 'SELL';
	quantity: string;
	price: string;
	fee: string;
	slippage: string;
	realized_pnl: string;
	timestamp: string;
}
