import { refreshAccessToken } from '../auth/auth';

let socket: WebSocket | null = null;
let reconnecting = false;

export async function connectEquitySocket(
	token: string,
	onMessage: (data: Record<string, unknown>) => void
) {
	if (socket) {
		socket.close();
	}

	socket = new WebSocket(
		`ws://localhost:8000/ws/equity?token=${encodeURIComponent(token)}`
	);

	socket.onmessage = (event) => {
		onMessage(JSON.parse(event.data));
	};

	socket.onclose = async (event) => {
		if (event.code === 1008 && !reconnecting) {
			reconnecting = true;

			try {
				const newToken = await refreshAccessToken();
				reconnecting = false;
				connectEquitySocket(newToken, onMessage);
			} catch {
				reconnecting = false;
				console.error('WS refresh failed — logging out');
			}
		}
	};

	socket.onerror = () => {
		socket?.close();
	};
}
