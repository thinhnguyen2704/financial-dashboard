import { useState } from 'react';
import api from '../api/client';
import { useAuth } from '../auth/useAuth';
import type { AuthResponse } from '../types/auth';

export default function Login() {
	const { setToken } = useAuth();
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	const handleLogin = async () => {
		const res = await api.post<AuthResponse>('/auth/login', {
			email,
			password,
		});

		const token = res.data.access_token;

		// ✅ Persist token
		localStorage.setItem('token', token);

		// ✅ Update in-memory auth state
		setToken(token);
	};

	return (
		<div>
			<input
				placeholder='Email'
				value={email}
				onChange={(e) => setEmail(e.target.value)}
			/>
			<input
				placeholder='Password'
				type='password'
				value={password}
				onChange={(e) => setPassword(e.target.value)}
			/>
			<button onClick={handleLogin}>Login</button>
		</div>
	);
}
