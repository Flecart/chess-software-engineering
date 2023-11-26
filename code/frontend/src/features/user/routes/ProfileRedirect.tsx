import { useAuth } from '@/features/auth';
import { useNavigate } from '@tanstack/react-router';
import { useEffect } from 'react';

export const ProfileRedirect = () => {
    const { username } = useAuth();

    // WORKAROUND: using the Navigate component directly, updates the URL but does not render the component
    // https://github.com/TanStack/router/issues/801
    // using the useNavigate hook, updates the URL and renders the component
    const navigate = useNavigate();
    useEffect(() => {
        navigate({ to: '/profile/$username', params: { username }, replace: true });
    });
    return <></>;
};
