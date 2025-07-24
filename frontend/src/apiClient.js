// src/api.js
import axios from 'axios';

// Django API'mizin ana adresi
const API_URL = 'http://127.0.0.1:8000';

// Axios için temel bir instance (örnek) oluşturuyoruz.
// Tüm istekler bu ayarları kullanacak.
const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true, // Tarayıcının cookie'leri (sessionid, csrftoken) göndermesini sağlar
});

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