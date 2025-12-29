import api from '../api/client';
import { useEffect, useState } from 'react';
import type { EquityData } from '../types/equity';
import { useEquityStream } from '../hooks/useEquityStream';

export default function Dashboard() {
	const [data, setData] = useState<EquityData[]>([]);
	const equity = useEquityStream();

	useEffect(() => {
		api.post('/backtest?ticker=AAPL').then((res) => {
			const formatted = Object.entries(res.data.equity).map(
				([date, equity]) => ({ date, equity: equity as number })
			);
			setData(formatted);
		});
	}, []);

	return (
		<div>
			<h2>Live Equity</h2>
			{equity && <p>{equity.toFixed(2)}</p>}
			{data.length > 0 && (
				<div>
					<h3>Backtest Data</h3>
					<ul>
						{data.map((item) => (
							<li key={item.date}>{item.date}: {item.equity}</li>
						))}
					</ul>
				</div>
			)}
		</div>
	);
}
