import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';
import { password, username } from '../hooks/auth';
import { useRegisterMutation } from '../hooks/useAuthMutation';

export const Register = () => {
    const { mutate, isPending } = useRegisterMutation();

    const action = () => mutate({ username: username.value, password: password.value });

    return (
        <>
            <Typography.Title>Registrati</Typography.Title>
            <AuthForm username={username} password={password} execAction={action} isLoading={isPending} />
        </>
    );
};
