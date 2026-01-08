import type { Trade } from "../types/trade";

export function TradeBlotter({ trades }: { trades: Trade[] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>Symbol</th>
          <th>Side</th>
          <th>Qty</th>
          <th>Price</th>
          <th>Realized PnL</th>
        </tr>
      </thead>
      <tbody>
        {trades.map((t, i) => (
          <tr key={i}>
            <td>{new Date(t.timestamp).toLocaleTimeString()}</td>
            <td>{t.symbol}</td>
            <td>{t.side}</td>
            <td>{t.quantity}</td>
            <td>{t.price}</td>
            <td>{t.realized_pnl}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
