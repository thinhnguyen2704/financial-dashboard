import type { EquitySnapshot } from '../types/equity';

export function connectEquitySocket(
	portfolioId: number,
	token: string,
	onMessage: (data: EquitySnapshot) => void
) {
	let socket: WebSocket;

	function connect() {
		socket = new WebSocket(
			`ws://localhost:8000/ws/equity/${portfolioId}?token=${token}`
		);

		socket.onmessage = (event) => {
			onMessage(JSON.parse(event.data));
		};

		socket.onclose = () => {
			setTimeout(connect, 1000); // auto-reconnect
		};
	}

	connect();

	return () => socket.close();
}
