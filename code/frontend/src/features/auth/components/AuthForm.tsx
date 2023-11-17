import { Button, Form, Input } from 'antd';

type FieldType = {
    username?: string;
    password?: string;
};

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
            <Form name="basic-auth" labelCol={{ span: 8 }} wrapperCol={{ span: 16 }} style={{ maxWidth: 600 }}>
                <Form.Item<FieldType>
                    label="Username"
                    name="username"
                    rules={[{ required: true, message: 'Please input your username!' }]}
                >
                    <Input onChange={onChangeUsername} />
                </Form.Item>

                <Form.Item<FieldType>
                    label="Password"
                    name="password"
                    rules={[{ required: true, message: 'Please input your password!' }]}
                >
                    <Input.Password onChange={onChangePassword} />
                </Form.Item>

                <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                    <Button type="primary" htmlType="submit" onClick={execAction}>
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        </>
    );
};
