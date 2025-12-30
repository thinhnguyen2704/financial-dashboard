import { useEffect } from 'react';
import { connectEquitySocket } from '../services/websocket';
import { connectRoleBasedSocket } from '../services/wsManager';
import { useAuth } from '../hooks/useAuth';

export default function Dashboard() {
	const { token, user } = useAuth();

	const setData = (data: Record<string, unknown>) => {
		console.log('Role-based update:', data);
	};

	useEffect(() => {
		if (!token) return;

		const ws = connectEquitySocket(token);

		ws.onmessage = (event) => {
			console.log('Equity update:', JSON.parse(event.data));
		};

		return () => ws.close();
	}, [token]);

	useEffect(() => {
		if (!token || !user || !user.role) return;

		connectRoleBasedSocket(token, user.role as 'user' | 'admin', setData);
	}, [token, user]);

	return <h2>Dashboard</h2>;
}
