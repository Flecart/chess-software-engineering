import { Button, Result } from 'antd';
import { useNavigate } from '@tanstack/react-router';

export const ToBeImplemented = () => {
    const navigate = useNavigate({ from: '/404' });
    return (
        <Result
            status="404"
            title="404"
            subTitle="La pagina che hai cercato non esiste."
            extra={
                <Button type="primary" onClick={() => navigate({ to: '/' })}>
                    Torna alla Home
                </Button>
            }
        />
    );
};
