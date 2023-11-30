import { useMutation } from '@tanstack/react-query';
import { postLogin, postRegister } from '../api/auth';
import { useTokenContext } from '@/lib/tokenContext';
import { useNavigate } from '@tanstack/react-router';

export const useLoginMutation = () => {
    const { setToken } = useTokenContext();
    const navigate = useNavigate({ from: '/login' as const });

    const loginMutation = useMutation({
        mutationFn: postLogin,
        onSuccess(data) {
            setToken(data);
            navigate({ to: '/' as const });
        },
        meta: {
            onSuccessMessage: 'Login effettuato con successo!',
        },
    });
    return loginMutation;
};

export const useRegisterMutation = () => {
    const { setToken } = useTokenContext();
    const navigate = useNavigate({ from: '/register' as const });

    const loginMutation = useMutation({
        mutationFn: postRegister,
        onSuccess(data) {
            setToken(data);
            navigate({ to: '/' as const });
        },
        meta: {
            onSuccessMessage: 'Registrazione effettuata con successo!',
        },
    });
    return loginMutation;
};
