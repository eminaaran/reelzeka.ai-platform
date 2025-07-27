import createApiClient from './client';
import type { LoginCredentials, RegisterCredentials, User, AuthResponse } from '../types/auth';

export const createAuthService = (platform = 'web') => {
    const apiClient = createApiClient(platform);

    return {
        login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
            const response = await apiClient.post('/login/', credentials);
            return response.data;
        },

        register: async (credentials: RegisterCredentials): Promise<AuthResponse> => {
            const response = await apiClient.post('/register/', credentials);
            return response.data;
        },

        logout: async (): Promise<void> => {
            await apiClient.post('/logout/');
        },

        getCurrentUser: async (): Promise<User> => {
            const response = await apiClient.get('/user/');
            return response.data;
        }
    };
};

export default { createAuthService };
