import { useState, useContext } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { TokenContext } from '@/lib/context';
import { AuthForm } from '../components/AuthForm';
import { postLogin } from '../api/auth';

export const Login = () => {
    const navigate = useNavigate({ from: '/login' });
    const { setToken } = useContext(TokenContext);
    const [usename, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = async () => {
        const token = await postLogin(usename, password);
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
