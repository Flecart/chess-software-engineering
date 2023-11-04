import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Game } from '@/features/chessboard';

const gameRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'game',
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

export const gameRoutes = gameRoute.addChildren([specificGameRoute]);
