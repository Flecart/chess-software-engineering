import { axios } from '@/lib/axios';

type Game = {
    'game-id': string;
};

type Move = {
    game_ended: boolean;
    board: string;
};

type Board = {
    has_enemy_moved: boolean;
    board: string;
};

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
