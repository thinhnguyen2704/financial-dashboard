export interface AuthContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

export interface User {
  id: number;
  email: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: "bearer";
}