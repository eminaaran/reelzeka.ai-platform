import axios from 'axios';

// API URL'ini ortam değişkenlerinden al
const API_URL = import.meta.env?.VITE_API_URL || 'http://127.0.0.1:8000/api';

const createApiClient = (platform = 'web') => {
    const apiClient = axios.create({
        baseURL: API_URL,
        withCredentials: platform === 'web', // Sadece web için cookie desteği
    });

    // Web platformu için CSRF token yönetimi
    if (platform === 'web') {
        apiClient.interceptors.request.use(
            (config) => {
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
                
                if (csrfToken) {
                    config.headers['X-CSRFToken'] = csrfToken;
                }
                
                return config;
            },
            (error) => {
                return Promise.reject(error);
            }
        );
    }

    return apiClient;
};

export default createApiClient;
