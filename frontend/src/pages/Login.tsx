import api from "../api/client";
import { useAuth } from "../auth/useAuth";

export default function Login() {
  const context = useAuth();

  const { setToken } = context;

  const login = async () => {
    const res = await api.post("/auth/login");
    setToken(res.data.access_token);
  };

  return <button onClick={login}>Login</button>;
}
