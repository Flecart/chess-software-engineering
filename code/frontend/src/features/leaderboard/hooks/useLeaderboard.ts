import { queryOptions, useQuery } from '@tanstack/react-query';
import { getLeaderBoard } from '../api/leaderboard';

export function leaderboardOptions() {
    return queryOptions({
        queryKey: ['leaderboard'],
        queryFn: () => getLeaderBoard(),
    });
}

export const useLeaderboardQuery = () => useQuery(leaderboardOptions());
