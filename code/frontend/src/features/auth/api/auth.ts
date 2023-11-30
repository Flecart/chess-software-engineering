import { axios } from '@/lib/axios';

import type { jwt_token } from '@/types';
import { AuthPayload } from '../types';

export async function postRegister(userData: AuthPayload): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/signup', userData);
    return response.data;
}

export async function postLogin(userData: AuthPayload): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/login', userData);
    return response.data;
}
