import { Profile } from '@/features/user';
import { ProfileRedirect } from '@/features/user/';
import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';

const profileRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'profile',
});

const indexProfileRoute = new Route({
    getParentRoute: () => profileRoute,
    path: '/',
    component: ProfileRedirect,
});

const specificProfileRoute = new Route({
    getParentRoute: () => profileRoute,
    path: '$username',
    component: Profile,
});

export const specificProfileRouteId = specificProfileRoute.id;

export const profileRoutes = profileRoute.addChildren([indexProfileRoute, specificProfileRoute]);
