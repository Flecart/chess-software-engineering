import type { User } from '@/features/user';
import { axios } from '@/lib/axios';

export async function getLeaderBoard(): Promise<User[]> {
    const response = await axios.get('/api/v1/user/leaderboard');
    return response.data;
}
