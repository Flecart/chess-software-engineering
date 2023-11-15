import { frontendUrl } from '@/config';
import { useNavigate } from '@tanstack/react-router';
import { Button, Flex, Modal, Typography } from 'antd';
import { useState } from 'react';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';

type Props = {
    useParams: () => { gameId?: string };
    useSearch: () => { boardOrientation?: 'white' | 'black' };
};

export const Game = ({ useParams, useSearch }: Props) => {
    const { gameId } = useParams();
    const { boardOrientation } = useSearch();
    if (!gameId) throw new Error('gameId is required');
    if (!boardOrientation) throw new Error('boardOrientation is required');
    const navigate = useNavigate({ from: '/game/$gameId' });
    const [isMyTurn, setIsMyTurn] = useState(boardOrientation === 'white');
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';
    const [gameEnded, setGameEnded] = useState(false);

    const gameIsEnded = () => {
        setGameEnded(true);
    };

    const resetGame = () => {
        setGameEnded(false);
    };

    const setUpNewGame = () => {
        resetGame();
        navigate({ to: '/game' });
    };

    return (
        <Flex wrap="wrap">
            <section style={{ width: '25%' }}>
                <Typography.Paragraph
                    copyable={{
                        text: `${frontendUrl}/game/${gameId}?boardOrientation=${opponentBoardOrientation}`,
                    }}
                >
                    Copia il link per invitare qualcuno
                </Typography.Paragraph>
            </section>

            <Flex vertical gap="small">
                <Typography.Title level={3} type={isMyTurn ? 'success' : 'danger'}>
                    {isMyTurn ? 'È il tuo turno' : "È il turno dell'avversario"}
                </Typography.Title>
                <PlayerInfo color={opponentBoardOrientation} myTurn={!isMyTurn} opponent />
                <Chessboard
                    gameId={gameId}
                    boardOrientation={boardOrientation}
                    setIsMyTurn={setIsMyTurn}
                    gameIsEnded={gameIsEnded}
                />
                <PlayerInfo color={boardOrientation} myTurn={isMyTurn} />
            </Flex>

            {/* Modal to show when game ends */}
            <Modal
                title="La partita è terminata"
                open={gameEnded}
                centered
                footer={[
                    <Button key="newGame" onClick={() => setUpNewGame()}>
                        Nuova partita
                    </Button>,
                    <Button key="backToHome" onClick={() => navigate({ to: '/' })}>
                        Torna alla home
                    </Button>,
                ]}
                onCancel={() => setUpNewGame()}
            >
                <p>Speriamo che tu ti sia divertito</p>
            </Modal>
        </Flex>
    );
};
