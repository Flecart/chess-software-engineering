import { Button, Form, Input } from 'antd';
import type { AuthPayload } from '../types';

type Props = {
    setUsername: (username: string) => void;
    setPassword: (password: string) => void;
    execAction: () => void;
};

export const AuthForm = ({ setUsername, setPassword, execAction }: Props) => {
    const onChangeUsername = (e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value);
    const onChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value);

    return (
        <>
            <Form name="basic-auth" wrapperCol={{ span: 16 }} style={{ maxWidth: 600 }} onFinish={execAction}>
                <Form.Item<AuthPayload>
                    label="Username"
                    name="username"
                    rules={[{ required: true, message: 'Inserisci il nome utente' }]}
                >
                    <Input onChange={onChangeUsername} />
                </Form.Item>

                <Form.Item<AuthPayload>
                    label="Password"
                    name="password"
                    rules={[{ required: true, message: 'Inserisci la password' }]}
                >
                    <Input.Password onChange={onChangePassword} />
                </Form.Item>

                <Form.Item wrapperCol={{ span: 16 }}>
                    <Button type="primary" htmlType="submit">
                        Conferma
                    </Button>
                </Form.Item>
            </Form>
        </>
    );
};
