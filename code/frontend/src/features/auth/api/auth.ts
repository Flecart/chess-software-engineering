import { axios } from '@/lib/axios';

export type jwt_token = string;

export async function postRegister(username: string, password: string): Promise<jwt_token> {
    //TODO: create a type for the response
    const response = await axios.post('/api/v1/user/signup', { username, password });
    return response.data;
}

export async function postLogin(username: string, password: string): Promise<jwt_token> {
    //TODO: create a type for the response
    const response = await axios.post('/api/v1/user/login', { username, password });
    return response.data;
}
