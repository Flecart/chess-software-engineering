import { Navigate, Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Profile } from '@/features/user';

const profileRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'profile',
});

const indexProfileRoute = new Route({
    getParentRoute: () => profileRoute,
    path: '/',
    component: () => {
        //TODO: redirect to logged user
        return <Navigate to="/profile/$username" params={{ username: 'magnus' }} replace />;
    },
});

const specificProfileRoute = new Route({
    getParentRoute: () => profileRoute,
    path: '$username',
    component: Profile,
});

export const specificProfileRouteId = specificProfileRoute.id;

export const profileRoutes = profileRoute.addChildren([indexProfileRoute, specificProfileRoute]);
