import type { GameResult, User } from '../types';
import { axios } from '@/lib/axios';

export async function getUser(username: string): Promise<User> {
    const response = await axios.get(`/api/v1/user/info/${username}`);
    return response.data;
}

export async function getUserGames(username: string): Promise<GameResult[]> {
    const response = await axios.get(`/api/v1/user/games/${username}`);
    return response.data;
}
