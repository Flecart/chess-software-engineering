import { RootRoute, Route, Router } from '@tanstack/react-router';
import { gameRoutes } from './game';

export const rootRoute = new RootRoute();

export const indexRoute = new Route({
    getParentRoute: () => rootRoute,
    path: '/',
    component: () => <h1>Landing Page</h1>,
});

const routeTree = rootRoute.addChildren([indexRoute, gameRoutes]);

export const router = new Router({ routeTree });

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router;
    }
}
