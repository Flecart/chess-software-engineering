import { queryOptions, useQuery } from '@tanstack/react-query';
import { getUser, getUserGames } from '../api/users';

function userOptions(username: string) {
    return queryOptions({
        queryKey: ['user', { username }],
        queryFn: () => getUser(username),
    });
}

function userGamesOptions(username: string) {
    return queryOptions({
        queryKey: ['user-games', { username }],
        queryFn: () => getUserGames(username),
    });
}

export const useUserQuery = (username: string) => useQuery(userOptions(username));

export const useUserGamesQuery = (username: string) => useQuery(userGamesOptions(username));
