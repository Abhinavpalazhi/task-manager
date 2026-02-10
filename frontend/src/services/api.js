import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Attach access token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Handle expired access token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If access token expired
    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken =
          localStorage.getItem("refresh_token");

        const res = await axios.post(
          "http://localhost:8000/auth/refresh",
          {
            refresh_token: refreshToken,
          }
        );

        // Save new access token
        localStorage.setItem(
          "access_token",
          res.data.access_token
        );

        // Retry original request with new token
        originalRequest.headers.Authorization =
          `Bearer ${res.data.access_token}`;

        return api(originalRequest);
      } catch (err) {
        // Refresh token failed → logout
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");

        window.location.href = "/login";
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
