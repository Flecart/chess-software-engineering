import { Profile } from '@/features/user';
import { ProfileRedirect } from '@/features/user/';
import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { RequireAuth } from '@/features/auth';

const profileRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'profile',
    component: RequireAuth,
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

export const profileRoutes = profileRoute.addChildren([indexProfileRoute, specificProfileRoute]);
