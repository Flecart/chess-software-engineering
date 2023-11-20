import { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';
import { postRegister } from '../api/auth';
import { useTokenContext } from '@/lib/tokenContext';

export const Register = () => {
    const navigate = useNavigate({ from: '/register' });
    const { setToken } = useTokenContext();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = async () => {
        const token = await postRegister(username, password);
        setToken(token);
        //TODO: handle errors
        navigate({ to: '/' });
    };

    return (
        <>
            <Typography.Title>Registrati</Typography.Title>
            <AuthForm setUsername={setUsername} setPassword={setPassword} execAction={action} />
        </>
    );
};
