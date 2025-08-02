// src/apiClient.js
import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true,
});

apiClient.interceptors.request.use(
    (config) => {
        const csrfToken = Cookies.get('csrftoken');
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Servisleri export etmeden önce ekle
export const chatService = {
    askQuestion: (query) => apiClient.post('/chatbot-query/', { query: query })
};

export default apiClient;