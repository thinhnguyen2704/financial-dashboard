import { useEffect, useState } from 'react';

export function useMarketData() {
	const [price, setPrice] = useState<number>();

	useEffect(() => {
		const ws = new WebSocket('ws://localhost:8000/ws/prices?token=JWT');

		ws.onmessage = (e) => {
			setPrice(JSON.parse(e.data).price);
		};

		return () => ws.close();
	}, []);

	return price;
}
