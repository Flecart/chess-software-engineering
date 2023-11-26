import { apiBaseUrl, wsUrl } from '@/config';
import { axios } from '@/lib/axios';
import type { jwt_token } from '@/types';
import { createCode, parseCode } from '../utils/code';

export async function loginAsGuest(): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/guest');
    return response.data;
}

export async function createGame(
    token: jwt_token,
    isBot: boolean = false,
    type: string = 'dark_chess',
): Promise<string> {
    const response = await axios.post<string>(
        `${apiBaseUrl}/game`,
        {
            against_bot: isBot,
            type,
        },
        { headers: { Authorization: token } },
    );
    return createCode(response.data);
}

export async function joinGame(
    token: jwt_token,
    gameId: string,
    color: null | 'white' | 'black' = null,
): Promise<void> {
    const colorParam = color ?? '';

    await axios.put(`${apiBaseUrl}/game/${parseCode(gameId)}/join/${colorParam}`, undefined, {
        headers: { Authorization: token },
    });
}

export function getWsUrl(gameId: string): string {
    return `${wsUrl}/api/v1/game/${parseCode(gameId)}/ws`;
}
