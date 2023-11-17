import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Register } from '@/features/auth';

const authRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'auth',
});

const registerRoute = new Route({
    getParentRoute: () => authRoute,
    path: 'register',
    component: Register,
});

export const authRoutes = authRoute.addChildren([registerRoute]);
