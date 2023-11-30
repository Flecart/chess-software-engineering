import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';
import { postRegister } from '../api/auth';
import { username, password } from '../hooks/auth';
import { useTokenContext } from '@/lib/tokenContext';

export const Register = () => {
    const navigate = useNavigate({ from: '/register' as const });
    const { setToken } = useTokenContext();

    const action = async () => {
        const token = await postRegister(username.value, password.value);
        setToken(token);
        //TODO: handle errors
        navigate({ to: '/' });
    };

    return (
        <>
            <Typography.Title>Registrati</Typography.Title>
            <AuthForm username={username} password={password} execAction={action} />
        </>
    );
};
