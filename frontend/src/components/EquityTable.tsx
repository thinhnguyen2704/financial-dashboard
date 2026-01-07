import type { EquitySnapshot } from "../types/equity";

export default function EquityTable({ snapshot }: { snapshot: EquitySnapshot }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Qty</th>
          <th>Avg Price</th>
          <th>Market</th>
          <th>Unrealized PnL</th>
        </tr>
      </thead>
      <tbody>
        {snapshot.positions.map((p) => (
          <tr key={p.symbol}>
            <td>{p.symbol}</td>
            <td>{p.quantity}</td>
            <td>{p.avg_price}</td>
            <td>{p.market_price}</td>
            <td>{p.unrealized_pnl}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
