import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8081/api/v1",
  timeout: 120000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (res) => res,
  (err) => Promise.reject(err)
);

export default api;
