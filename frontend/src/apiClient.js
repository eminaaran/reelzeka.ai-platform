// src/apiClient.js
import { createAuthService } from '../../shared/api';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true,
});

// Auth service
const authService = createAuthService('web');

// Test API İstekleri
export const testService = {
    fetchTests: async () => {
        const response = await apiClient.get('/tests/');
        return response.data;
    },

    fetchTest: async (testId) => {
        const response = await apiClient.get(`/tests/${testId}/`);
        return response.data;
    },

    submitTest: async (testId, answers) => {
        const response = await apiClient.post(`/tests/${testId}/submit/`, answers);
        return response.data;
    },

    fetchMyResults: async () => {
        const response = await apiClient.get('/tests/my-results/');
        return response.data;
    }
};

// Bu bir "interceptor". Her istek gönderilmeden HEMEN ÖNCE çalışır.
// Görevi, Django'dan aldığımız CSRF token'ını isteğin header'ına eklemektir.
apiClient.interceptors.request.use(
    (config) => {
        // Tarayıcının cookie'lerinden CSRF token'ını bul ve al
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
        }
        
        const csrfToken = getCookie('csrftoken');
        
        // Eğer token varsa, isteğin header'ına ekle
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default apiClient;