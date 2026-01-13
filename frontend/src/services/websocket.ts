import type { EquitySnapshot } from '../types/equity';

type EquityMessage =
	| { type: 'equity_history'; data: EquitySnapshot[] }
	| ({ type: 'equity_update' } & EquitySnapshot);

export function connectPortfolioEquitySocket(
	portfolioId: number,
	token: string,
	{
		onHistory,
		onUpdate,
	}: {
		onHistory: (history: EquitySnapshot[]) => void;
		onUpdate: (snapshot: EquitySnapshot) => void;
	}
): WebSocket {
	const ws = new WebSocket(
		`ws://localhost:8000/ws/portfolio/${portfolioId}?token=${encodeURIComponent(
			token
		)}`
	);

	ws.onopen = () => {
		console.log('Portfolio equity WebSocket connected');
	};

	ws.onmessage = (event) => {
		const msg: EquityMessage = JSON.parse(event.data);

		if (msg.type === 'equity_history') {
			onHistory(msg.data);
		}

		if (msg.type === 'equity_update') {
			onUpdate(msg);
		}
	};

	ws.onclose = () => {
		console.log('Portfolio equity WebSocket disconnected');
	};

	ws.onerror = (err) => {
		console.error('Portfolio equity WebSocket error', err);
	};

	return ws;
}
