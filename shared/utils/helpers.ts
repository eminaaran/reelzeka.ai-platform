// Validation utils
export const validateUsername = (username: string): boolean => {
    return username.length >= 3;
};

export const validatePassword = (password: string): boolean => {
    return password.length >= 8;
};

// Error handling utils
export const getErrorMessage = (error: any): string => {
    if (error.response) {
        // Server tarafından dönen hata
        const data = error.response.data;
        if (typeof data === 'string') return data;
        if (data.message) return data.message;
        if (data.detail) return data.detail;
        if (typeof data === 'object') {
            const firstError = Object.values(data)[0];
            if (Array.isArray(firstError)) return firstError[0] as string;
        }
    }
    return 'Bir hata oluştu. Lütfen tekrar deneyin.';
};

// Storage utils
export const storage = {
    set: (key: string, value: any): void => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage error:', e);
        }
    },
    
    get: <T>(key: string, defaultValue: T | null = null): T | null => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Storage error:', e);
            return defaultValue;
        }
    },
    
    remove: (key: string): void => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Storage error:', e);
        }
    }
};
