import { router } from '@/routes';
import { RouterProvider } from '@tanstack/react-router';

export const App = () => {
    return <RouterProvider router={router} />;
};
