// frontend/src/api.js (İçeriği bu şekilde olmalı)
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api'; // API adresimizin kökü

const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true, // Cookie'lerin gönderilmesi için KRİTİK ayar
});

// Cookie okuma fonksiyonu
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Her istekten önce çalışan Interceptor
apiClient.interceptors.request.use(
    (config) => {
        const csrfToken = getCookie('csrftoken');
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default apiClient;