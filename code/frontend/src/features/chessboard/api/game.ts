import { axios } from '@/lib/axios';
import { wsUrl } from '@/config';
import type { jwt_token } from '@/types';
import { apiBaseUrl } from '@/config';

type Game = {
    'game-id': string;
};

type GameId = string;

type Move = {
    game_ended: boolean;
    board: string;
};

type Board = {
    has_enemy_moved: boolean;
    board: string;
};

type JoinResponse =
    | {
          error: string;
      }
    | {
          data: string;
      };

export async function loginAsGuest(): Promise<jwt_token> {
    const response = await axios.post('/api/v1/user/guest');
    return response.data;
}

export async function createGame(
    token: jwt_token,
    isBot: boolean = false,
    type: string = 'dark_chess',
): Promise<GameId> {
    const response = await axios.post<string>(
        `${apiBaseUrl}/game`,
        {
            against_bot: isBot,
            type,
        },
        { headers: { Authorization: token } },
    );
    return response.data;
}

export async function joinGame(
    token: jwt_token,
    gameId: string,
    color: null | 'white' | 'black' = null,
): Promise<string> {
    let response: JoinResponse | null = null;
    if (color === null) {
        response = await axios.put(`${apiBaseUrl}/game/${gameId}/join/`, undefined, {
            headers: { Authorization: token },
        });
    } else {
        response = await axios.put(`${apiBaseUrl}/game/${gameId}/join/${color}`, undefined, {
            headers: { Authorization: token },
        });
    }

    if (response === null || 'error' in response) {
        throw Error(response ? response.error : 'error in joining game');
    }

    return `${wsUrl}/api/v1/game/${gameId}/${token}/ws`;
}

export function getWsUrl(gameId: string, token: jwt_token): string {
    return `${wsUrl}/api/v1/game/${gameId}/${token}/ws`;
}

export async function startGame(): Promise<Game> {
    const response = await axios.get('/game/start');
    return response.data;
}

export async function makeMove(gameId: string, move: string): Promise<Move> {
    const response = await axios.get(`/game/${gameId}/move/${move}`);
    return response.data;
}

export async function getBoard(gameId: string, color: 'white' | 'black'): Promise<Board> {
    const response = await axios.get(`/game/${gameId}/board/${color}`);
    return response.data;
}
