import { useTokenContext } from '@/lib/tokenContext';
import { Navigate, Outlet } from '@tanstack/react-router';
import { useIsGuest } from '../hooks/useIsGuest';

export const RequireAuth = () => {
    const { token } = useTokenContext();
    const isGuest = useIsGuest(token);
    const isAuthenticated = token !== null && !isGuest;

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};
