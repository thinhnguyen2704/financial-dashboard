import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import type { EquityPoint } from '../types/charts';
import { ResponsiveContainer } from 'recharts';
interface Props {
	data: EquityPoint[];
}

export function EquityChart({ data }: Props) {
	return (
		<ResponsiveContainer width='100%' height={300}>
			<LineChart data={data}>
				<XAxis dataKey='timestamp' />
				<YAxis />
				<Tooltip />
				<Line type='monotone' dataKey='equity' strokeWidth={2} dot={false} />
			</LineChart>
		</ResponsiveContainer>
	);
}
