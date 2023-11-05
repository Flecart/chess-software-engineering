import { frontendUrl } from '@/config';
import { UserOutlined } from '@ant-design/icons';
import { useNavigate } from '@tanstack/react-router';
import { Avatar, Button, Flex, Typography } from 'antd';
import { startGame } from '../api/game';
import { Chessboard } from '../components/Chessboard';

type Props = {
    useParams: () => { gameId?: string };
    useSearch: () => { boardOrientation?: 'white' | 'black' };
};

export const Game = ({ useParams, useSearch }: Props) => {
    const { gameId } = useParams();
    const { boardOrientation } = useSearch();
    const navigate = useNavigate({ from: '/game' });
    const gameStarted = !!gameId && !!boardOrientation;
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';

    return (
        <>
            <h1>Game started: {String(gameStarted)}</h1>
            <Button
                disabled={gameStarted}
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

            {gameStarted && (
                <Typography.Paragraph
                    copyable={{ text: `${frontendUrl}/game/${gameId}?boardOrientation=${opponentBoardOrientation}` }}
                >
                    Copia il link per invitare qualcuno
                </Typography.Paragraph>
            )}
            {gameStarted && (
                <Flex vertical gap="small" style={{ margin: '0 auto', width: 'fit-content' }}>
                    <Flex align="center" gap="small" style={{ flexDirection: 'row-reverse' }}>
                        <Avatar shape="square" icon={<UserOutlined />} />
                        <p>{boardOrientation === 'black' ? 'Bianco' : 'Nero'}</p>
                        {/* space filler */}
                        <div style={{ width: '100%' }}></div>
                        <div style={{ border: '1px solid', borderRadius: '3px', padding: '3px' }}>Timer</div>
                    </Flex>
                    <Chessboard gameId={gameId} boardOrientation={boardOrientation} />
                    <Flex align="center" gap="small">
                        <Avatar shape="square" icon={<UserOutlined />} />
                        <p>{boardOrientation === 'black' ? 'Nero' : 'Bianco'}</p>
                        {/* space filler */}
                        <div style={{ width: '100%' }}></div>
                        <div style={{ border: '1px solid', borderRadius: '3px', padding: '3px' }}>Timer</div>
                    </Flex>
                </Flex>
            )}
        </>
    );
};
