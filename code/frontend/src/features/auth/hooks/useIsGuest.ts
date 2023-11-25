import { jwtDecode } from 'jwt-decode';
import { useMemo } from 'react';

export const useIsGuest = (token: string | null) => {
    const isGuest = useMemo(() => {
        if (!token) return false;
        const decodedToken = jwtDecode(token);
        // check if the decoded token has guest property
        return 'guest' in decodedToken && typeof decodedToken.guest === 'boolean' && decodedToken.guest;
    }, [token]);
    return isGuest;
};
