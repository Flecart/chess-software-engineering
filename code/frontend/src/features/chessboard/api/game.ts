import { apiBaseUrl, wsUrl } from '@/config';
import { axios } from '@/lib/axios';
import type { jwt_token } from '@/types';
import type { color } from '../types';
import { CreateGameParams } from '../types';
import { createCode, parseCode } from '../utils/code';

export async function loginAsGuest(): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/guest');
    return response.data;
}

export async function createGame(
    token: jwt_token,
    isBot: boolean = false,
    type: 'dark_chess' | 'kriegspiel' = 'dark_chess',
    time: number = 0,
): Promise<string> {
    const params: CreateGameParams = {
        against_bot: isBot,
        type,
        time,
    };
    const response = await axios.post<string>(`${apiBaseUrl}/game`, params, { headers: { Authorization: token } });
    return createCode(response.data);
}

export async function joinGame(token: jwt_token, gameId: string, color: null | color = null): Promise<color> {
    const colorParam = color ?? '';

    const response = await axios.put(`${apiBaseUrl}/game/${parseCode(gameId)}/join/${colorParam}`, undefined, {
        headers: { Authorization: token },
    });
    return response.data.color;
}

export function getWsUrl(gameId: string): string {
    return `${wsUrl}/api/v1/game/${parseCode(gameId)}/ws`;
}

// Darkboard related functions

type PollResponse = {
    fen: string
}

export async function startDarkboard(): Promise<void> {
    console.log("starting darkboard");
    await axios.post(`${apiBaseUrl}/darkboard/start`);
}

export async function poll(): Promise<PollResponse> {
    const response = await axios.get<PollResponse>(`${apiBaseUrl}/darkboard/status`);
    console.log("here is the data" + JSON.stringify(response.data));
    return response.data as unknown as PollResponse;
}

export async function makeBotMove(): Promise<void> {
    await axios.post(`${apiBaseUrl}/darkboard/move`);
}