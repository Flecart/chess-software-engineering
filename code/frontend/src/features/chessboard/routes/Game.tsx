import { frontendUrl } from '@/config';
import { useNavigate } from '@tanstack/react-router';
import { Button, Flex, Typography } from 'antd';
import { useState } from 'react';
import { startGame } from '../api/game';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';

type Props = {
    useParams: () => { gameId?: string };
    useSearch: () => { boardOrientation?: 'white' | 'black' };
};

export const Game = ({ useParams, useSearch }: Props) => {
    const { gameId } = useParams();
    const { boardOrientation } = useSearch();
    const navigate = useNavigate({ from: '/game' });
    const [isMyTurn, setIsMyTurn] = useState(boardOrientation === 'white');
    const gameStarted = !!gameId && !!boardOrientation;
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';
    console.log('Game rendered');

    return (
        <Flex wrap="wrap">
            <section style={{ width: '25%' }}>
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
                        copyable={{
                            text: `${frontendUrl}/game/${gameId}?boardOrientation=${opponentBoardOrientation}`,
                        }}
                    >
                        Copia il link per invitare qualcuno
                    </Typography.Paragraph>
                )}
            </section>
            {gameStarted && (
                <Flex vertical gap="small">
                    <Typography.Title level={3} type={isMyTurn ? 'success' : 'danger'}>
                        {isMyTurn ? 'È il tuo turno' : "È il turno dell'avversario"}
                    </Typography.Title>
                    <PlayerInfo color={opponentBoardOrientation} myTurn={!isMyTurn} opponent />
                    <Chessboard gameId={gameId} boardOrientation={boardOrientation} setIsMyTurn={setIsMyTurn} />
                    <PlayerInfo color={boardOrientation} myTurn={isMyTurn} />
                </Flex>
            )}
        </Flex>
    );
};
