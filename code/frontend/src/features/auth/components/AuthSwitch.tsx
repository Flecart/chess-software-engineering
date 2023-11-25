import { useTokenContext } from '@/lib/tokenContext';
import { useIsGuest } from '..';

type Props = {
    AuthComponent: () => JSX.Element;
    UnauthComponent: () => JSX.Element;
};
export const AuthSwitch = ({ AuthComponent, UnauthComponent }: Props) => {
    const NewComponent = () => {
        const { token } = useTokenContext();
        const isGuest = useIsGuest(token);
        const isAuthenticated = token !== null && !isGuest;

        return isAuthenticated ? <AuthComponent /> : <UnauthComponent />;
    };
    return NewComponent;
};
