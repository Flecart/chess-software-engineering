import { Outlet, useNavigate } from '@tanstack/react-router';
import { useEffect } from 'react';
import { AuthSwitch } from '../components/AuthSwitch';

export const RequireAuth = AuthSwitch({
    AuthComponent: () => <Outlet />,
    UnauthComponent: () => {
        // WORKAROUND: using the Navigate component directly, updates the URL but does not render the component
        // https://github.com/TanStack/router/issues/801
        // using the useNavigate hook, updates the URL and renders the component

        const navigate = useNavigate();
        useEffect(() => {
            navigate({ to: '/login', replace: true });
        });
        return <></>;
    },
});
