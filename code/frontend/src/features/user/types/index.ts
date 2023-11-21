export type User = {
    username: string;
    avatar: string;
    elo: number;
    wins: number;
    losses: number;
};

export type GameResult = {
    opponentName: string;
    opponentAvatar: string;
    opponentElo: number;
    result: 'win' | 'loss';
    eloGain: number;
    id: string;
};
