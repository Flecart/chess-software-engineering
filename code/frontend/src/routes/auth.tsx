import { AuthSwitch, HomeRedirect, Login, Register } from '@/features/auth';
import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';

export const registerRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'register',
    component: AuthSwitch({
        AuthComponent: HomeRedirect,
        UnauthComponent: Register,
    }),
});

export const loginRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'login',
    component: AuthSwitch({
        AuthComponent: HomeRedirect,
        UnauthComponent: Login,
    }),
});
