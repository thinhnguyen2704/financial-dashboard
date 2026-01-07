import { useEffect, useState } from 'react';
import { connectEquitySocket } from '../api/equitySocket';
import type { EquitySnapshot } from '../types/equity';
import EquityTable from '../components/EquityTable';
import EquityChart from '../components/EquityChart';

interface EquityHistoryPoint {
	date: string;
	equity: number;
}

export default function PortfolioLive() {
	const [snapshot, setSnapshot] = useState<EquitySnapshot | null>(null);
	const [history, setHistory] = useState<EquityHistoryPoint[]>([]);

	useEffect(() => {
		const disconnect = connectEquitySocket(
			1, // portfolio_id
			'JWT_TOKEN_HERE', // auth
			(data) => {
				setSnapshot(data);
				setHistory((h) => [
					...h.slice(-100),
					{
						date: new Date(data.timestamp).toLocaleString(),
						equity: Number(data.equity),
					},
				]);
			}
		);

		return disconnect;
	}, []);

	if (!snapshot) return <div>Loading...</div>;

	return (
		<>
			<h2>Total Equity: {snapshot.equity}</h2>
			<EquityChart data={history} />
			<EquityTable snapshot={snapshot} />
		</>
	);
}
