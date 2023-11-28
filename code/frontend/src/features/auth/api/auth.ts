import { axios } from '@/lib/axios';

import type { jwt_token } from '@/types';

export async function postRegister(username: string, password: string): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/signup', { username, password });
    return response.data;
}

export async function postLogin(username: string, password: string): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/login', { username, password });
    return response.data;
}
