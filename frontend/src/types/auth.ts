export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

export interface User {
  email: string;
  role?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: "bearer";
}