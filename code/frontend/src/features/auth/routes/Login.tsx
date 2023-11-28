import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';
import { postLogin } from '../api/auth';
import { username, password } from '../hooks/auth';
import { useTokenContext } from '@/lib/tokenContext';

export const Login = () => {
    const navigate = useNavigate({ from: '/login' as const });
    const { setToken } = useTokenContext();

    const action = async () => {
        const token = await postLogin(username.value, password.value);
        setToken(token);
        //TODO: handle errors
        navigate({ to: '/' });
    };

    return (
        <>
            <Typography.Title>Accedi</Typography.Title>
            <AuthForm username={username} password={password} execAction={action} />
        </>
    );
};
