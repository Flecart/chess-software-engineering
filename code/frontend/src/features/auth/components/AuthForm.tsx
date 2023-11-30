import { Button, Form, Input } from 'antd';
import type { Signal } from '@preact/signals-react';
import type { AuthPayload } from '../types';
import { LoadingOutlined } from '@ant-design/icons';

type Props = Readonly<{
    username: Signal<string>;
    password: Signal<string>;
    isLoading?: boolean;
    execAction: () => void;
}>;

export const AuthForm = ({ username, password, isLoading, execAction }: Props) => {
    const onChangeUsername = (e: React.ChangeEvent<HTMLInputElement>) => (username.value = e.target.value);
    const onChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => (password.value = e.target.value);

    return (
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
                    {isLoading && <LoadingOutlined spin />}
                    Conferma
                </Button>
            </Form.Item>
        </Form>
    );
};
