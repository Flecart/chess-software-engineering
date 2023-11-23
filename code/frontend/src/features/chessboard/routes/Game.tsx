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

// TODO: maybe we need to differentiate the response types, because
// now we mix the repsponse with the beginning of the game, with those of the game
type GameState = {
    ended: boolean;
    possible_moves: null | string[];
    view: string;
    move_made: null | string;
    turn: 'white' | 'black';

    // TODO: refactor next sprint
    time_left_white: string | null
    time_left_black: string | null
    time_start_white: string | null
    time_start_black: string | null
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

    const [myTimeRemaining, setMyTimeRemaining] = useState<number>(0); 
    const [opponentTimeRemaining, setOpponentTimeRemaining] = useState<number>(0);
    

    // TODO: refactor me, serve solametne per non fartire il timer quando il bianco non ha ancora fatto la mossa
    // const [isFirstMoveMade, setIsFirstMoveMade] = useState<boolean>(boardOrientation === 'white');

    function parseTimeDelta(timeDelta: string): number {
        const parts = timeDelta.split(/[:.]/);
        if (parts.length < 3) throw new Error('Invalid time delta');
        // TODO: a volte c'è anche millisecondi, non sempre, non lo stiamo gestendo, non 
        // so se è importante, forse non si nota.

        const hours = parseInt(parts[0] as string, 10);
        const minutes = parseInt(parts[1] as string, 10);
        const seconds = parseInt(parts[2] as string, 10);

        const totalSeconds = hours * 60 * 60 + minutes * 60 + seconds;

        return totalSeconds;
    }

    const endTimeCallback = () => {
        console.log("enttime callback");
        // Deve essere fatta una richiesta per triggerare l'endgame
        makeMove('a1', 'a1'); // mossa arbitraria a caso, utilizzata per ricevere la risposta e finire il gioco
    }

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

        if (lastJsonMessage !== null && 'ended' in lastJsonMessage) {
            let myRemainingTime = "";
            let opponentRemainingTime = "";
            if (boardOrientation === 'white') {
                myRemainingTime = lastJsonMessage.time_left_white as string;
                opponentRemainingTime = lastJsonMessage.time_left_black as string;
            } else {
                myRemainingTime = lastJsonMessage.time_left_black as string;
                opponentRemainingTime = lastJsonMessage.time_left_white as string;
            }
            setMyTimeRemaining(parseTimeDelta(myRemainingTime));
            setOpponentTimeRemaining(parseTimeDelta(opponentRemainingTime));

            if (lastJsonMessage.ended) {
                setGameEnded(true);
            }
        }

        // questo è necessario per non andare in loop infinito di update
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [lastJsonMessage]);

    const makeMove = (from: string, to: string) => {
        if (isMyTurn) {
            sendJsonMessage({ kind: 'move', data: `${from}${to}` });
            setIsFirstMoveMade(true);
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
                    Se giochi con una altra persona, condividi l'ID {gameId}!
                </Typography.Paragraph>
            </section>

            {/* <pre>{JSON.stringify(lastJsonMessage, null, 2)}</pre> */}

            <Flex vertical gap="small">
                <Typography.Title level={3} type={isMyTurn ? 'success' : 'danger'}>
                    {isMyTurn ? 'È il tuo turno' : "È il turno dell'avversario"}
                </Typography.Title>
                <PlayerInfo color={opponentBoardOrientation} 
                    myTurn={!isMyTurn} 
                    timeRemaining={opponentTimeRemaining} 
                    timerStopping={isMyTurn} opponent 
                />
                    <Chessboard
                        fen={fen}
                        boardOrientation={boardOrientation}
                        makeMove={makeMove}
                        gameIsEnded={gameIsEnded}
                    />
                <PlayerInfo color={boardOrientation} 
                    myTurn={isMyTurn} 
                    timeRemaining={myTimeRemaining}
                    timerStopping={!isMyTurn}
                    timerEndCallback={endTimeCallback}
                />
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
