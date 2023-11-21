import { useTokenContext } from '@/lib/tokenContext';
import { specificGameRouteId } from '@/routes/game';
import { useNavigate, useParams, useSearch } from '@tanstack/react-router';
import { Button, Flex, Modal, Typography } from 'antd';
import { useEffect, useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { getWsUrl } from '../api/game';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { parseCode } from '../utils/code';

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../????????/????????/????????/????????';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
// ^ white fen is '????????/????????/????????/????????/......../......../PPPPPPPP/RNBQKBNR';

type GameState = {
    ended: boolean;
    possible_moves: null | string[];
    view: string;
    move_made: null | string;
    turn: 'white' | 'black';
};

type WaitingState = {
    waiting: true;
};

type wsMessage = GameState | WaitingState | null;

export const Game = () => {
    const { gameId } = useParams({ from: specificGameRouteId });
    const { boardOrientation } = useSearch({ from: specificGameRouteId });
    const navigate = useNavigate({ from: specificGameRouteId });
    const { token } = useTokenContext();

    // TODO: gestire meglio questo, dovrà essere in useEffect, e l'errore mostrato (magari un redirecto?)
    if (!token) throw new Error('Token not found');

    const [isMyTurn, setIsMyTurn] = useState(boardOrientation !== 'white');
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';
    const [gameEnded, setGameEnded] = useState(false);

    const { lastJsonMessage, sendJsonMessage } = useWebSocket<wsMessage>(getWsUrl(parseCode(gameId), token));
    const [fen, setFen] = useState<string>(boardOrientation === 'white' ? startWhiteFEN : startBlackFEN);

    useEffect(() => {
        if (isMyTurn) {
            if (lastJsonMessage && 'move_made' in lastJsonMessage && lastJsonMessage.move_made !== null) {
                setFen(lastJsonMessage.view);
                setIsMyTurn(false);
            }
        } else if (lastJsonMessage && !('waiting' in lastJsonMessage)) {
            setFen(lastJsonMessage.view);
            setIsMyTurn(true);
        }

        if (lastJsonMessage !== null && 'ended' in lastJsonMessage && lastJsonMessage.ended) {
            setGameEnded(true);
        }
        // questo è necessario per non andare in loop infinito di update
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [lastJsonMessage]);

    const makeMove = (from: string, to: string) => {
        if (isMyTurn) {
            sendJsonMessage({ kind: 'move', data: `${from}${to}` });
        }
        // l'aggiornamento del turno è fatto dall'effect
    };

    const gameIsEnded = () => {
        setGameEnded(true);
    };

    const resetGame = () => {
        setGameEnded(false);
    };

    const setUpNewGame = () => {
        resetGame();
        navigate({ to: '/game', search: { bot: true } });
    };

    return (
        <Flex wrap="wrap">
            <section style={{ width: '30%' }}>
                <Typography.Paragraph
                    copyable={{
                        text: gameId,
                    }}
                >
                    Condividi l'id di Gioco con l'altra persona! {gameId}
                </Typography.Paragraph>
            </section>

            {/* <pre>{JSON.stringify(lastJsonMessage, null, 2)}</pre> */}

            <Flex vertical gap="small">
                <Typography.Title level={3} type={isMyTurn ? 'success' : 'danger'}>
                    {isMyTurn ? 'È il tuo turno' : "È il turno dell'avversario"}
                </Typography.Title>
                <PlayerInfo color={opponentBoardOrientation} myTurn={!isMyTurn} opponent />
                <Chessboard
                    fen={fen}
                    boardOrientation={boardOrientation}
                    makeMove={makeMove}
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
