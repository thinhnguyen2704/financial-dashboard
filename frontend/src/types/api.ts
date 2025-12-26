import type { EquityPoint } from "./charts";

export interface BacktestResponse {
  equity: Record<string, number>;
}

export interface EquitySeriesResponse {
  points: EquityPoint[];
}
