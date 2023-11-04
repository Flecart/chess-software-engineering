import { Layout } from '@/components/Layout';
import { RootRoute, Route, Router } from '@tanstack/react-router';
import { gameRoutes } from './game';
import { ToBeImplemented } from '@/features/misc/';

export const rootRoute = new RootRoute({ component: Layout });

export const indexRoute = new Route({
    getParentRoute: () => rootRoute,
    path: '/',
    component: () => <h1>Landing Page</h1>,
});

export const notFoundRoute = new Route({
    getParentRoute: () => rootRoute,
    path: '404',
    component: ToBeImplemented,
});

const routeTree = rootRoute.addChildren([indexRoute, gameRoutes, notFoundRoute]);

export const router = new Router({ routeTree });

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router;
    }
}
