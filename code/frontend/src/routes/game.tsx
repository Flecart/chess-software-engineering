import { Game, Pregame } from '@/features/chessboard';
import type { GameRouteSearch, PregameRouteSearch } from '@/types';
import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';

const gameRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'game',
});

const indexGameRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '/',
    component: Pregame,
    validateSearch: (search): PregameRouteSearch => {
        return { bot: 'bot' in search && (search.bot === 'true' || search.bot === true) };
    },
});

const specificGameRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '$gameId',
    component: Game,
    validateSearch: (search): GameRouteSearch => {
        return { boardOrientation: search.boardOrientation === 'white' ? 'white' : 'black' };
    },
});

export const gameRoutes = gameRoute.addChildren([indexGameRoute, specificGameRoute]);
