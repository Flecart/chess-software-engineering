export const backendUrl = (import.meta.env.VITE_BACKEND_URL as string) ?? 'http://localhost:8000';
export const frontendUrl = (import.meta.env.VITE_FRONTEND_URL as string) ?? 'http://localhost:5173';

export const wsUrl = backendUrl.replace(/^http/, 'ws');
export const apiBaseUrl = '/api/v1';
