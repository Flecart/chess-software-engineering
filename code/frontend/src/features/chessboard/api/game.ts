import { axios } from '@/lib/axios';

type Game = {
    'game-id': string;
};

export async function startGame(): Promise<Game> {
    const response = await axios.get('/game/start');
    return response.data;
}

type Move = {
    game_ended: boolean;
    board: string;
};

export async function makeMove(gameId: string, move: string): Promise<Move> {
    const response = await axios.get(`/game/${gameId}/move/${move}`);
    return response.data;
}
