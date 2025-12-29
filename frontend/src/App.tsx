import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import { AuthProvider } from './auth/AuthProvider';
import { useAuth } from './hooks/useAuth';

function ProtectedRoute({ children }: { children: React.JSX.Element }) {
	const { user } = useAuth();

	if (!user) {
		return <Navigate to='/login' replace />;
	}

	return children;
}

export default function App() {
	return (
		<AuthProvider>
			<BrowserRouter>
				<Routes>
					<Route path='/login' element={<Login />} />
					<Route path='/signup' element={<Signup />} />

					<Route
						path='/dashboard'
						element={
							<ProtectedRoute>
								<Dashboard />
							</ProtectedRoute>
						}
					/>

					<Route path='*' element={<Navigate to='/login' replace />} />
				</Routes>
			</BrowserRouter>
		</AuthProvider>
	);
}
