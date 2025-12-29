import { useState } from 'react';
import axios from 'axios';

interface SignupResponse {
	id: number;
	email: string;
}

export default function Signup() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [error, setError] = useState<string | null>(null);
	const [loading, setLoading] = useState(false);
	const [success, setSuccess] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError(null);

		if (password.length < 8) {
			setError('Password must be at least 8 characters.');
			return;
		}

		if (password.length > 72) {
			setError('Password must be 72 characters or fewer.');
			return;
		}

		if (password !== confirmPassword) {
			setError('Passwords do not match.');
			return;
		}

		try {
			setLoading(true);

			await axios.post<SignupResponse>('http://localhost:8000/auth/signup', {
				email,
				password,
			});

			setSuccess(true);
		} catch (err) {
			if (axios.isAxiosError(err)) {
				setError(err.response?.data?.detail ?? 'Signup failed');
			} else {
				setError('Unexpected error occurred');
			}
		} finally {
			setLoading(false);
		}
	};

	if (success) {
		return (
			<div style={{ maxWidth: 400, margin: '0 auto' }}>
				<h2>Account Created</h2>
				<p>You can now log in with your credentials.</p>
				<a href='/login'>Go to Login</a>
			</div>
		);
	}

	return (
		<div style={{ maxWidth: 400, margin: '0 auto' }}>
			<h2>Sign Up</h2>

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

				<input
					type='password'
					placeholder='Confirm Password'
					value={confirmPassword}
					required
					onChange={(e) => setConfirmPassword(e.target.value)}
				/>

				{error && <p style={{ color: 'red' }}>{error}</p>}

				<button type='submit' disabled={loading}>
					{loading ? 'Creating account...' : 'Sign Up'}
				</button>
			</form>
			<p>
				Already have an account? <a href='/login'>Login</a>
			</p>
		</div>
	);
}
