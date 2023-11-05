import { Layout } from '@/components/Layout';
import { RootRoute, Route, Router } from '@tanstack/react-router';
import { gameRoutes } from './game';
import { Landing, ToBeImplemented } from '@/features/misc/';
import { RouterDevtools } from '@/components/RouterDevtools';

export const rootRoute = new RootRoute({
    component: () => (
        <>
            <Layout />
            <RouterDevtools />
        </>
    ),
});

export const indexRoute = new Route({
    getParentRoute: () => rootRoute,
    path: '/',
    component: Landing,
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
