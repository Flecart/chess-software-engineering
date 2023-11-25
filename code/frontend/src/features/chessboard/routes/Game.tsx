import { useTokenContext } from '@/lib/tokenContext';
import { specificGameRouteId } from '@/routes/game';
import { useNavigate, useParams, useSearch } from '@tanstack/react-router';
import { Button, Flex, Modal, Typography } from 'antd';
import useWebSocket from 'react-use-websocket';
import { getWsUrl } from '../api/game';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { parseTimeDelta } from '../utils/time';
import type { wsMessage } from '../types';
import { isMyTurn, gameEnded, fen } from '../hooks/gamestate';
import { myRemainingTime, myTimeStart, opponentRemainingTime, opponentTimeStart } from '../hooks/timer';

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../????????/????????/????????/????????';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
// ^ white fen is '????????/????????/????????/????????/......../......../PPPPPPPP/RNBQKBNR';

export const Game = () => {
    const { gameId } = useParams({ from: specificGameRouteId });
    const { boardOrientation } = useSearch({ from: specificGameRouteId });
    const navigate = useNavigate({ from: specificGameRouteId });
    const { token } = useTokenContext();

    // TODO: gestire meglio questo, dovrà essere in useEffect, e l'errore mostrato (magari un redirecto?)
    if (!token) throw new Error('Token not found');

    isMyTurn.value = boardOrientation !== 'white';
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';
    gameEnded.value = false;
    fen.value = boardOrientation === 'white' ? startWhiteFEN : startBlackFEN;
    myRemainingTime.value = 0;
    opponentRemainingTime.value = 0;
    myTimeStart.value = null;
    opponentTimeStart.value = null;
    const { sendJsonMessage } = useWebSocket<wsMessage>(getWsUrl(gameId, token), {
        onMessage: (event) => {
            const message = JSON.parse(event.data) as wsMessage;
            if (isMyTurn.value) {
                if (message && 'move_made' in message && message.move_made !== null) {
                    fen.value = message.view;
                    isMyTurn.value = false;
                }
            } else if (message && !('waiting' in message)) {
                fen.value = message.view;
                isMyTurn.value = true;
            }

            if (message !== null && 'ended' in message) {
                let myTimeRemaining = '';
                let opponentTimeRemaining = '';
                let myStartTime: string | null = null;
                let opponentStartTime: string | null = null;
                if (boardOrientation === 'white') {
                    myTimeRemaining = message.time_left_white as string;
                    opponentTimeRemaining = message.time_left_black as string;
                    myStartTime = message.time_start_white;
                    opponentStartTime = message.time_start_black;
                } else {
                    myTimeRemaining = message.time_left_black as string;
                    opponentTimeRemaining = message.time_left_white as string;
                    myStartTime = message.time_start_black;
                    opponentStartTime = message.time_start_white;
                }
                myRemainingTime.value = parseTimeDelta(myTimeRemaining);
                opponentRemainingTime.value = parseTimeDelta(opponentTimeRemaining);
                myTimeStart.value = myStartTime;
                opponentTimeStart.value = opponentStartTime;
                if (message.ended) gameEnded.value = true;
            }
        },
    });

    const endTimeCallback = () => {
        console.log('enttime callback');
        // Deve essere fatta una richiesta per triggerare l'endgame
        makeMove('a1', 'a1'); // mossa arbitraria a caso, utilizzata per ricevere la risposta e finire il gioco
    };

    const makeMove = (from: string, to: string) => {
        if (isMyTurn.value) sendJsonMessage({ kind: 'move', data: `${from}${to}` });
        // l'aggiornamento del turno è fatto dall'effect
    };

    const gameIsEnded = () => (gameEnded.value = true);

    const resetGame = () => (gameEnded.value = false);

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

            <Flex vertical gap="small">
                <Typography.Title level={3} type={isMyTurn.value ? 'success' : 'danger'}>
                    {isMyTurn.value ? 'È il tuo turno' : "È il turno dell'avversario"}
                </Typography.Title>
                <PlayerInfo
                    color={opponentBoardOrientation}
                    myTurn={!isMyTurn.value}
                    timeRemaining={opponentRemainingTime.value}
                    timerStopping={opponentTimeStart.value === null}
                    opponent
                />
                <Chessboard
                    fen={fen.value}
                    boardOrientation={boardOrientation}
                    makeMove={makeMove}
                    gameIsEnded={gameIsEnded}
                />
                <PlayerInfo
                    color={boardOrientation}
                    myTurn={isMyTurn.value}
                    timeRemaining={myRemainingTime.value}
                    timerStopping={myTimeStart.value === null}
                    timerEndCallback={endTimeCallback}
                />
            </Flex>

            {/* Modal to show when game ends */}
            <Modal
                title="La partita è terminata"
                open={gameEnded.value}
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
