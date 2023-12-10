import { useNavigate } from '@tanstack/react-router';
import { Button, Flex } from 'antd';

export const ButtonSection = () => {
    const navigate = useNavigate({ from: '/' as const });

    return (
        <>
            <Flex justify="center" gap={100} wrap="wrap" style={{ width: '100%', marginTop: '120px' }}>
                <Button
                    type="primary"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game/', search: { bot: true } });
                    }}
                >
                    Gioca contro il computer
                </Button>
                <Button
                    type="default"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game/', search: { bot: false } });
                    }}
                >
                    Gioca Online
                </Button>
            </Flex>
            <Flex justify="center" gap={100} wrap="wrap" style={{ width: '100%', marginTop: '2rem' }}>
                <Button
                    type="primary"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/darkboard' });
                    }}
                >
                    Guarda Darkboard - OpenSpiel
                </Button>
            </Flex>
        </>
    );
};
