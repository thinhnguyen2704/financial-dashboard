import { useEffect } from "react";
import { connectEquitySocket } from "../services/websocket";
import { useAuth } from "../hooks/useAuth";

export default function Dashboard() {
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;

    const ws = connectEquitySocket(token);

    ws.onmessage = (event) => {
      console.log("Equity update:", JSON.parse(event.data));
    };

    return () => ws.close();
  }, [token]);

  return <h2>Dashboard</h2>;
}
