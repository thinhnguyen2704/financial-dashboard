import { useEffect, useState } from 'react';
import { connectPortfolioEquitySocket } from '../services/websocket';
import type { EquitySnapshot } from '../types/equity';
import type { EquityPoint } from '../types/charts';

const MAX_POINTS = 300;

export function useEquityStream(portfolioId: number, token: string) {
	const [equitySeries, setEquitySeries] = useState<EquityPoint[]>([]);
	const [latestEquity, setLatestEquity] = useState<number | null>(null);

	useEffect(() => {
		if (!portfolioId || !token) return;

		const ws = connectPortfolioEquitySocket(portfolioId, token, {
			onHistory: (history: EquitySnapshot[]) => {
				const points: EquityPoint[] = history.map((snap) => ({
					date: snap.timestamp,
					equity: Number(snap.equity),
				}));

				setEquitySeries(points.slice(-MAX_POINTS));

				if (points.length > 0) {
					setLatestEquity(points[points.length - 1].equity);
				}
			},

			onUpdate: (snap: EquitySnapshot) => {
				const point: EquityPoint = {
					date: snap.timestamp,
					equity: Number(snap.equity),
				};

				setLatestEquity(point.equity);

				setEquitySeries((prev) => [...prev.slice(-MAX_POINTS), point]);
			},
		});

		return () => ws.close();
	}, [portfolioId, token]);

	return {
		equitySeries,
		latestEquity,
	};
}
