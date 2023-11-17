import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Leaderboard } from '@/features/leaderboard';

export const leaderboardRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'leaderboard',
    component: Leaderboard,
});
