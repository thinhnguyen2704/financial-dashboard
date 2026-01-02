import { useEffect, useState } from 'react';
import { connectEquitySocket } from '../services/wsManager';
import type { PnLMessage } from '../types/websocket';

export default function PnLWidget({ token }: { token: string }) {
	const [pnl, setPnl] = useState<number>(0);

	useEffect(() => {
		connectEquitySocket<PnLMessage>(
			token,
			(msg) => {
				setPnl(msg.pnl);
			},
			'/ws/pnl'
		);
	}, [token]);

	return <h3>PnL: ${pnl.toFixed(2)}</h3>;
}
