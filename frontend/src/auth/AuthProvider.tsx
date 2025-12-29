import { useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import type { User } from '../types/auth';
import { AuthContext } from './authContext';

interface JwtPayload {
	sub: string;
	role?: string;
}

function decodeUser(token: string | null): User | null {
  if (!token) return null;

  try {
    const decoded = jwtDecode<JwtPayload>(token);
    return {
      email: decoded.sub,
      role: decoded.role,
    };
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem("token")
  );

  const [user, setUser] = useState<User | null>(() => decodeUser(token));

  const login = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUser(decodeUser(newToken));
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}