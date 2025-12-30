import { useState } from 'react';
import axios from 'axios';

interface LoginResponse {
	access_token: string;
	refresh_token?: string;
}

export default function Login() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState<string | null>(null);
	const [loading, setLoading] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError(null);

		if (password.length > 72) {
			setError('Password must be 72 characters or fewer.');
			return;
		}

		if (password.length < 8) {
			setError('Password must be at least 8 characters.');
			return;
		}

		try {
			setLoading(true);

			const res = await axios.post<LoginResponse>(
				'http://localhost:8000/auth/login',
				{ email, password }
			);

			localStorage.setItem('token', res.data.access_token);

			if (res.data.refresh_token) {
				localStorage.setItem('refresh_token', res.data.refresh_token);
			}

			window.location.href = '/dashboard';
		} catch (err: unknown) {
			if (axios.isAxiosError(err)) {
				setError(err.response?.data?.detail ?? 'Login failed');
			} else {
				setError('Unexpected error occurred');
			}
		} finally {
			setLoading(false);
		}
	};

	return (
		<div style={{ maxWidth: 400, margin: '0 auto' }}>
			<h2>Login</h2>

			<form onSubmit={handleSubmit}>
				<input
					type='email'
					placeholder='Email'
					value={email}
					required
					onChange={(e) => setEmail(e.target.value)}
				/>

				<input
					type='password'
					placeholder='Password'
					value={password}
					required
					onChange={(e) => setPassword(e.target.value)}
				/>

				{error && <p style={{ color: 'red' }}>{error}</p>}

				<button type='submit' disabled={loading}>
					{loading ? 'Signing in...' : 'Login'}
				</button>
			</form>
			<p>
				Don't have an account? <a href='/signup'>Sign up</a>
			</p>
		</div>
	);
}
