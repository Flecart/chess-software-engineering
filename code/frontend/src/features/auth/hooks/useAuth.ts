import { useTokenContext } from '@/lib/tokenContext';
import { jwtDecode } from 'jwt-decode';
import { useMemo } from 'react';

export const useAuth = () => {
    const { token } = useTokenContext();

    const result = useMemo(() => {
        const defName = 'magnus';
        if (!token) return { isAuth: false, isGuest: false, username: defName };

        const decodedToken = jwtDecode(token);

        if (
            ('guest' in decodedToken && typeof decodedToken.guest === 'boolean' && decodedToken.guest) ||
            !('sub' in decodedToken) ||
            !decodedToken.sub
        ) {
            return { isAuth: false, isGuest: true, username: defName };
        }

        return { isAuth: true, isGuest: false, username: decodedToken.sub };
    }, [token]);

    return result;
};
