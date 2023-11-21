import type { User } from '@/features/user';
// import { axios } from '@/lib/axios';

export async function getLeaderBoard(): Promise<User[]> {
    // TODO: do real api call
    // const response = await axios.get('/leaderboard');
    // return response.data;

    return Array.from({ length: 10 }, (_, i) => ({
        username: `User${i + 1}`,
        elo: Math.floor(Math.random() * 2000),
        avatar: `https://api.dicebear.com/7.x/croodles/svg?seed=${i + 1}`,
        wins: Math.floor(Math.random() * 100),
        losses: Math.floor(Math.random() * 100),
    }));
}
