import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Game } from '@/features/chessboard';

const gameRoute = new Route({ getParentRoute: () => rootRoute, path: 'game' });
// TODO: this solution is not the greatest, but it works for now
export const gameIndexRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '/',
    component: Game,
});

export const specificGameRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '$gameId',
    component: Game,
    validateSearch: (search): { boardOrientation?: 'white' | 'black' } => {
        return { boardOrientation: search.boardOrientation === 'white' ? 'white' : 'black' };
    },
});

export const gameRoutes = gameRoute.addChildren([gameIndexRoute, specificGameRoute]);
