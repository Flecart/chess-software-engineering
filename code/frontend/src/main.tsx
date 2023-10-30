import { ConfigProvider as AntdConfigProvider } from 'antd';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Game } from './features/chessboard/index.ts';
import './index.css';
import { RootRoute, Route, Router, RouterProvider } from '@tanstack/react-router';

const rootRoute = new RootRoute();

const indexRoute = new Route({ getParentRoute: () => rootRoute, path: '/', component: () => <div>index</div> });
const gameRoute = new Route({ getParentRoute: () => rootRoute, path: 'game' });
const gameIndexRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '/',
    component: Game,
});

const specificGameRoute = new Route({
    getParentRoute: () => gameRoute,
    path: '$gameId',
    component: Game,
});

const routeTree = rootRoute.addChildren([indexRoute, gameRoute.addChildren([gameIndexRoute, specificGameRoute])]);

const router = new Router({ routeTree });

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router;
    }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        {/* Customize theme */}
        <AntdConfigProvider>
            <RouterProvider router={router} />
        </AntdConfigProvider>
    </React.StrictMode>,
);
