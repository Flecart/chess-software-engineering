import { axios } from '@/lib/axios';

export async function postRegister(username: string, password: string): Promise<unknown> {
    //TODO: create a type for the response
    const response = await axios.post('/auth/register', { username, password });
    return response.data;
}

export async function postLogin(username: string, password: string): Promise<unknown> {
    //TODO: create a type for the response
    const response = await axios.post('/auth/login', { username, password });
    return response.data;
}
