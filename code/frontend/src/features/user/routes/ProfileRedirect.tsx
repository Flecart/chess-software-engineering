import { useAuth } from '@/features/auth';
import { Navigate } from '@tanstack/react-router';

export const ProfileRedirect = () => {
    const { username } = useAuth();

    return <Navigate to="/profile/$username" params={{ username }} replace />;
};
