import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Pregame, Game } from '@/features/chessboard';

const gameRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'game',
});

const indexGameRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '/',
    component: Pregame,
});

export const specificGameRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '$gameId',
    component: Game,
    validateSearch: (search): { boardOrientation?: 'white' | 'black' } => {
        return { boardOrientation: search.boardOrientation === 'white' ? 'white' : 'black' };
    },
});

export const gameRoutes = gameRoute.addChildren([indexGameRoute, specificGameRoute]);
