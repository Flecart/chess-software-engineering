import { QueryClient } from '@tanstack/react-query';
import type { AxiosError } from 'axios';

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 1000 * 60 * 15,
        },
    },
});

declare module '@tanstack/react-query' {
    interface Register {
        defaultError: AxiosError;
    }
}
