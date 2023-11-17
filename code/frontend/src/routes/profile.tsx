import { Route } from '@tanstack/react-router';
import { rootRoute } from '.';
import { Profile } from '@/features/user';

export const profileRoute = new Route({
    getParentRoute: () => rootRoute,
    path: 'profile',
    component: Profile,
});

// export const profileRoutes = ProfileRoute;
