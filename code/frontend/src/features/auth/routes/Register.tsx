import { useState } from 'react';

import { AuthForm } from '../components/AuthForm';

import { postRegister } from '../api/auth';

export const Register = () => {
    const [usename, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const action = () => {
        postRegister(usename, password);
        //TODO: handle errors
    };

    return (
        <>
            <AuthForm setUsername={setUsername} setPassword={setPassword} execAction={action} />
        </>
    );
};
