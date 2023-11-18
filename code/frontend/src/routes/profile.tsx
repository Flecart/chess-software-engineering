import { Navigate, Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Profile } from '@/features/user';

export const profileRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'profile',
});

export const indexProfileRoute = new Route({
    getParentRoute: () => profileRoute,
    path: '/',
    component: () => {
        //TODO: redirect to logged user
        return <Navigate to="/profile/$username" params={{ username: 'magnus' }} />;
    },
});

export const specificProfileRoute = new Route({
    getParentRoute: () => profileRoute,
    path: '$username',
    component: Profile,
});

export const profileRoutes = profileRoute.addChildren([indexProfileRoute, specificProfileRoute]);
