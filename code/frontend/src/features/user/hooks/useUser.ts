import { queryOptions, useQuery } from '@tanstack/react-query';
import { getUser, getUserGames } from '../api/users';

export function userOptions(username: string, enabled?: boolean) {
    return queryOptions({
        queryKey: ['user', { username }],
        queryFn: () => getUser(username),
        enabled,
    });
}

export function userGamesOptions(username: string) {
    return queryOptions({
        queryKey: ['user-games', { username }],
        queryFn: () => getUserGames(username),
    });
}

export const useUserQuery = (username: string, enabled?: boolean) => useQuery(userOptions(username, enabled));

export const useUserGamesQuery = (username: string) => useQuery(userGamesOptions(username));
