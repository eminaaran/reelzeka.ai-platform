import apiClient from '../apiClient';

export const adminService = {
    // Tüm modelleri listele
    getModels: async () => {
        try {
            const response = await apiClient.get('/admin/models/');
            return response.data;
        } catch (error) {
            console.error('Error fetching models:', error);
            throw error;
        }
    },

    // Belirli bir model için tüm kayıtları getir
    getModelEntries: async (modelId) => {
        try {
            const response = await apiClient.get(`/admin/models/${modelId}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching model entries:', error);
            throw error;
        }
    },

    // Model metadata bilgilerini getir
    getModelMetadata: async (modelId) => {
        try {
            const response = await apiClient.get(`/admin/models/${modelId}/model_metadata/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching model metadata:', error);
            throw error;
        }
    },

    // Yeni kayıt oluştur
    createEntry: async (modelId, data) => {
        try {
            const response = await apiClient.post(`/admin/models/${modelId}/create_object/`, data);
            return response.data;
        } catch (error) {
            console.error('Error creating entry:', error);
            throw error;
        }
    },

    // Kayıt güncelle
    updateEntry: async (modelId, data) => {
        try {
            const response = await apiClient.put(`/admin/models/${modelId}/update_object/`, data);
            return response.data;
        } catch (error) {
            console.error('Error updating entry:', error);
            throw error;
        }
    },

    // Kayıt sil
    deleteEntry: async (modelId, id) => {
        try {
            const response = await apiClient.delete(`/admin/models/${modelId}/delete_object/`, {
                data: { id }
            });
            return response.data;
        } catch (error) {
            console.error('Error deleting entry:', error);
            throw error;
        }
    }
};
