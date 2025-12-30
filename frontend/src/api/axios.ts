import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.response.use(
  res => res,
  async error => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem("refresh_token");
      if (!refresh) throw error;

      const res = await axios.post(
        "http://localhost:8000/auth/refresh",
        { token: refresh }
      );

      localStorage.setItem("token", res.data.access_token);
      error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
      return api(error.config);
    }
    throw error;
  }
);

export default api;
