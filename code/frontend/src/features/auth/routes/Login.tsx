import { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';
import { postLogin } from '../api/auth';
import { useTokenContext } from '@/lib/tokenContext';

export const Login = () => {
    const navigate = useNavigate({ from: '/login' });
    const { setToken } = useTokenContext();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = async () => {
        const token = await postLogin(username, password);
        setToken(token);
        //TODO: handle errors
        navigate({ to: '/' });
    };

    return (
        <>
            <Typography.Title>Accedi</Typography.Title>
            <AuthForm setUsername={setUsername} setPassword={setPassword} execAction={action} />
        </>
    );
};
