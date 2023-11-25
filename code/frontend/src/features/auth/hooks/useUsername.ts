import { jwtDecode } from 'jwt-decode';
import { useMemo } from 'react';

export const useUsername = (token: string | null) => {
    const username = useMemo(() => {
        const defValue = 'magnus';
        if (!token) return defValue;
        const decodedToken = jwtDecode(token);
        if (!('sub' in decodedToken) || !decodedToken.sub || decodedToken.sub.startsWith('guest')) {
            return defValue;
        }

        return decodedToken.sub;
    }, [token]);
    return username;
};
