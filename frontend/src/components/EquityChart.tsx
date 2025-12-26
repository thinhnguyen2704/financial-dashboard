import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";
import type { EquityPoint } from "../types/charts";

interface Props {
  data: EquityPoint[];
}

export default function EquityChart({ data }: Props) {
  return (
    <LineChart width={600} height={300} data={data}>
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="equity" />
    </LineChart>
  );
}
