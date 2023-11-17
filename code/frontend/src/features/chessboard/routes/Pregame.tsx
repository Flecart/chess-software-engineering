import { Button, Flex, Typography } from 'antd';
import { startGame } from '../api/game';
import { useNavigate } from '@tanstack/react-router';

export const Pregame = () => {
    const navigate = useNavigate({ from: '/game/' });
    return (
        <Flex wrap="wrap">
            <section style={{ width: '25%' }}>
                <Typography.Paragraph>Scegli il tempo</Typography.Paragraph>
                <Button
                    onClick={async () => {
                        const res = await startGame();
                        navigate({
                            to: '/game/$gameId',
                            params: { gameId: res['game-id'] },
                            search: { boardOrientation: 'white' },
                        });
                    }}
                >
                    Start Game
                </Button>
            </section>
        </Flex>
    );
};
