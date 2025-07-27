// src/services/testService.js
import apiClient from '../apiClient';

export const testService = {
    // Tüm testleri getir
    fetchTests: async () => {
        try {
            const response = await apiClient.get('/api/tests/');
            return response.data;
        } catch (error) {
            console.error('Error fetching tests:', error);
            throw error;
        }
    },

    // Belirli bir testi getir
    fetchTest: async (testId) => {
        try {
            const response = await apiClient.get(`/api/tests/${testId}/`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching test ${testId}:`, error);
            throw error;
        }
    },

    // Test sonucunu gönder
    submitTest: async (testId, answers) => {
        try {
            const response = await apiClient.post(`/api/tests/${testId}/submit/`, answers);
            return response.data;
        } catch (error) {
            console.error(`Error submitting test ${testId}:`, error);
            throw error;
        }
    }
};
