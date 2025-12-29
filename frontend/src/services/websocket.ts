export function connectEquitySocket(token: string): WebSocket {
  const ws = new WebSocket(
    `ws://localhost:8000/ws/equity?token=${encodeURIComponent(token)}`
  );

  ws.onopen = () => {
    console.log("WebSocket connected");
  };

  ws.onclose = () => {
    console.log("WebSocket disconnected");
  };

  ws.onerror = (err) => {
    console.error("WebSocket error", err);
  };

  return ws;
}
