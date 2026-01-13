import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { connectPortfolioEquitySocket } from '../services/websocket';
import { connectRoleBasedSocket } from '../services/wsManager';
import { useAuth } from '../hooks/useAuth';
import { EquityChart } from '../components/EquityChart';
import { type EquityPoint } from '../types/charts';

export default function Dashboard() {
	const { token, user } = useAuth();
	const { portfolioId } = useParams<{ portfolioId: string }>();
	const [equitySeries, setEquitySeries] = useState<EquityPoint[]>([]);
	const wsRef = useRef<WebSocket | null>(null);
	const numericPortfolioId = Number(portfolioId);

	const setData = (data: Record<string, unknown>) => {
		console.log('Role-based update:', data);
	};

	useEffect(() => {
		if (!token || !numericPortfolioId) return;
		wsRef.current = connectPortfolioEquitySocket(numericPortfolioId, token, {
			onHistory: (history) => {
				setEquitySeries(
					history.map((s) => ({
						date: s.timestamp,
						equity: Number(s.equity),
					}))
				);
			},
			onUpdate: (snap) => {
				setEquitySeries((prev) => [
					...prev,
					{
						date: snap.timestamp,
						equity: Number(snap.equity),
					},
				]);
			},
		});

		return () => wsRef.current?.close();
	}, [numericPortfolioId, token]);

	useEffect(() => {
		if (!token || !user || !user.role) return;

		connectRoleBasedSocket(token, user.role as 'user' | 'admin', setData);
	}, [token, user]);

	return (
		<>
			<h2>Dashboard</h2>
			<EquityChart data={equitySeries} />
		</>
	);
}
