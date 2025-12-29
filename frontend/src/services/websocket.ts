export function createEquitySocket() {
  return new WebSocket("ws://localhost:8000/ws/equity");
}
