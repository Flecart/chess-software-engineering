import { Navigate, Outlet } from '@tanstack/react-router';
import { useAuth } from '../hooks/useAuth';

export const RequireAuth = () => {
    const { isAuth } = useAuth();

    return isAuth ? <Outlet /> : <Navigate to="/login" replace />;
};
