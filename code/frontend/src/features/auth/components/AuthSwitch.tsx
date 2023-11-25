import { useAuth } from '../hooks/useAuth';

type Props = {
    AuthComponent: () => JSX.Element;
    UnauthComponent: () => JSX.Element;
};
export const AuthSwitch = ({ AuthComponent, UnauthComponent }: Props) => {
    const NewComponent = () => {
        const { isAuth } = useAuth();

        return isAuth ? <AuthComponent /> : <UnauthComponent />;
    };
    return NewComponent;
};
