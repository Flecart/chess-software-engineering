import { lazy, Suspense } from 'react';

const TanStackRouterDevtools = import.meta.env.PROD
    ? () => null // Render nothing in production
    : lazy(() =>
          // Lazy load in development
          import('@tanstack/router-devtools').then((res) => ({
              default: res.TanStackRouterDevtools,
          })),
      );

export const RouterDevtools = () => (
    <Suspense fallback={null}>
        <TanStackRouterDevtools position="bottom-right" />
    </Suspense>
);
