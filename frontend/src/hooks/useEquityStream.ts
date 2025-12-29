import { useEffect, useState } from "react";
import { createEquitySocket } from "../services/websocket";

export function useEquityStream() {
  const [equity, setEquity] = useState<number | null>(null);

  useEffect(() => {
    const ws = createEquitySocket();

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEquity(data.equity);
    };

    return () => {
      ws.close();
    };
  }, []);

  return equity;
}
