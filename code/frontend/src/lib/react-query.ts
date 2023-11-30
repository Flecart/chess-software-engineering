import { MutationCache, QueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';
import type { AxiosError } from 'axios';
import { ErrorResponseData, MutationMeta } from '@/types';

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 1000 * 60 * 15,
        },
    },
    mutationCache: new MutationCache({
        onError(error) {
            const errorData = error.response?.data;
            let errorMessage = 'Errore sconosciuto, riprova più tardi.';
            if (isErrorResponse(errorData)) errorMessage = errorData.message;
            toast.error(errorMessage);
        },
        onSuccess(_error, _variables, _context, mutation) {
            toast.success(mutation.meta?.onSuccessMessage ?? 'Operazione effettuata con successo!');
        },
    }),
});

declare module '@tanstack/react-query' {
    interface Register {
        defaultError: AxiosError;
    }
}

declare module '@tanstack/react-query' {
    interface Register {
        mutationMeta: MutationMeta;
    }
}

function isErrorResponse(obj: unknown): obj is ErrorResponseData {
    return typeof obj === 'object' && obj !== null && 'message' in obj && typeof obj.message === 'string';
}
