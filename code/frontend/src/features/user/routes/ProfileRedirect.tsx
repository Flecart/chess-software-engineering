import { useUsername } from '@/features/auth';
import { useTokenContext } from '@/lib/tokenContext';
import { Navigate } from '@tanstack/react-router';

export const ProfileRedirect = () => {
    const { token } = useTokenContext();
    const username = useUsername(token);

    return <Navigate to="/profile/$username" params={{ username }} replace />;
};
