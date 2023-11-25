import { useTokenContext } from '@/lib/tokenContext';
import { Navigate } from '@tanstack/react-router';
import { jwtDecode } from 'jwt-decode';
import { useMemo } from 'react';

export const ProfileRedirect = () => {
    const { token } = useTokenContext();

    const username = useMemo(() => {
        const defValue = 'magnus';
        if (!token) return defValue;
        const decodedToken = jwtDecode(token);
        if (!('sub' in decodedToken) || !decodedToken.sub || decodedToken.sub.startsWith('guest')) {
            return defValue;
        }

        return decodedToken.sub;
    }, [token]);

    return <Navigate to="/profile/$username" params={{ username }} replace />;
};
