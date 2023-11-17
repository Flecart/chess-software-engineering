import { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { Flex, Typography } from 'antd';

import { AuthForm } from '../components/AuthForm';

import { postRegister } from '../api/auth';

export const Register = () => {
    const navigate = useNavigate({ from: '/auth/register' });
    const [usename, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = () => {
        postRegister(usename, password);
        //TODO: handle errors
        navigate({ to: '/' });
    };

    return (
        <>
            <Typography.Title>Register</Typography.Title>
            <AuthForm setUsername={setUsername} setPassword={setPassword} execAction={action} />
        </>
    );
};
