import { useNavigate } from '@tanstack/react-router';
import { useEffect } from 'react';

export const HomeRedirect = () => {
    const navigate = useNavigate();
    useEffect(() => {
        navigate({ to: '/', replace: true });
    });
    return <></>;
};
