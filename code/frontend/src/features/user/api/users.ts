import type { GameResult, User } from '../types';

export async function getUser(username: string): Promise<User> {
    // TODO: implement api call
    // await new Promise((r) => setTimeout(r, 1000));
    return {
        username,
        elo: 1000,
        wins: 6,
        losses: 4,
        avatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${username}`,
    };
}

export async function getUserGames(username: string): Promise<GameResult[]> {
    // TODO: implement api call
    username;
    // await new Promise((r) => setTimeout(r, 1000));
    return [
        {
            opponentName: 'Player1',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 1500,
            result: 'win',
            eloGain: 10,
            id: '1',
        },
        {
            opponentName: 'Player2',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 1600,
            result: 'loss',
            eloGain: -10,
            id: '2',
        },
        {
            opponentName: 'Player3',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 1700,
            result: 'win',
            eloGain: +15,
            id: '3',
        },
        {
            opponentName: 'Player4',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 1800,
            result: 'loss',
            eloGain: -15,
            id: '4',
        },
        {
            opponentName: 'Player5',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 1900,
            result: 'win',
            eloGain: 20,
            id: '5',
        },
        {
            opponentName: 'Player6',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 2000,
            result: 'win',
            eloGain: 25,
            id: '6',
        },
        {
            opponentName: 'Player7',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 2100,
            result: 'loss',
            eloGain: -20,
            id: '7',
        },
        {
            opponentName: 'Player8',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 2200,
            result: 'win',
            eloGain: 30,
            id: '8',
        },
        {
            opponentName: 'Player9',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 2300,
            result: 'loss',
            eloGain: -25,
            id: '9',
        },
        {
            opponentName: 'Player10',
            opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
            opponentElo: 2400,
            result: 'win',
            eloGain: 35,
            id: '10',
        },
    ];
}
