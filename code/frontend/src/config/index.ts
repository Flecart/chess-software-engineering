export const protocol = (import.meta.env.VITE_PROTOCOL as string) ?? 'http';
export const wsProtocol = (import.meta.env.VITE_WS_PROTOCOL as string) ?? 'ws';
export const host = (import.meta.env.VITE_HOST as string) ?? 'localhost:8000';

export const backendUrl = `${protocol}://${host}`;
export const wsUrl = `${wsProtocol}://${host}`;

export const frontendUrl = (import.meta.env.VITE_FRONTEND_URL as string) ?? 'http://localhost:5173';

export const apiBaseUrl = '/api/v1';
