import axios from 'axios';

const API_URL = 'http://localhost:8000';

interface RefreshResponse {
	access_token: string;
}

export async function refreshAccessToken(): Promise<string> {
	const refreshToken = localStorage.getItem('refresh_token');

	if (!refreshToken) {
		throw new Error('No refresh token available');
	}

	const response = await axios.post<RefreshResponse>(
		`${API_URL}/auth/refresh`,
		{
			token: refreshToken,
		}
	);

	const newAccessToken = response.data.access_token;

	localStorage.setItem('token', newAccessToken);

	return newAccessToken;
}
