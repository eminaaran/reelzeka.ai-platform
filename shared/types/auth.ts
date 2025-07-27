// User types
export interface User {
    id: number;
    username: string;
    email?: string;
    is_staff?: boolean;
}

// Authentication types
export interface LoginCredentials {
    username: string;
    password: string;
}

export interface RegisterCredentials extends LoginCredentials {
    password2?: string;
}

export interface AuthResponse {
    user: User;
    token?: string;
}

// API Response types
export interface ApiResponse<T> {
    data: T;
    message?: string;
    status: number;
}

export interface ApiError {
    message: string;
    code?: string;
    field?: string;
}
