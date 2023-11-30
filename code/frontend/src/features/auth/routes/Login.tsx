import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';
import { password, username } from '../hooks/auth';
import { useLoginMutation } from '../hooks/useAuthMutation';

export const Login = () => {
    const { mutate, isPending } = useLoginMutation();

    const action = () => mutate({ username: username.value, password: password.value });

    return (
        <>
            <Typography.Title>Accedi</Typography.Title>
            <AuthForm username={username} password={password} execAction={action} isLoading={isPending} />
        </>
    );
};
