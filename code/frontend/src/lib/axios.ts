import { backendUrl } from '@/config';
import DefaultAxios from 'axios';

export const axios = DefaultAxios.create({
    baseURL: backendUrl,
    headers: {
        'Content-Type': 'application/json',
    },
});
