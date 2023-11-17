import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Register, Login } from '@/features/auth';

export const registerRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'register',
    component: Register,
});

export const loginRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'login',
    component: Login,
});
