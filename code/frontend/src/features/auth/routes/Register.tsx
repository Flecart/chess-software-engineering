import { useState, useContext } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { TokenContext } from '@/lib/context';
import { AuthForm } from '../components/AuthForm';
import { postRegister } from '../api/auth';

export const Register = () => {
    const navigate = useNavigate({ from: '/register' });
    const { setToken } = useContext(TokenContext);
    const [usename, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = async () => {
        const token = await postRegister(usename, password);
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
