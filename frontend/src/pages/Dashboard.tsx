import api from "../api/client";
import { useEffect, useState } from "react";
import EquityChart from "../components/EquityChart";

export default function Dashboard() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    api.post("/backtest?ticker=AAPL").then(res => {
      const formatted = Object.entries(res.data.equity).map(
        ([date, equity]: any) => ({ date, equity })
      );
      setData(formatted);
    });
  }, []);

  return <EquityChart data={data} />;
}
