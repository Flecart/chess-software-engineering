import { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';

import { postLogin } from '../api/auth';

export const Login = () => {
    const navigate = useNavigate({ from: '/auth/login' });
    const [usename, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = () => {
        postLogin(usename, password);
        //TODO: handle errors
        navigate({ to: '/' });
    };

    return (
        <>
            <Typography.Title>Log in</Typography.Title>
            <AuthForm setUsername={setUsername} setPassword={setPassword} execAction={action} />
        </>
    );
};
