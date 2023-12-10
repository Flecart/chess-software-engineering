import { TwitterShareButton } from '@/features/social';
import { useTokenContext } from '@/lib/tokenContext';
import { useNavigate, useParams, useSearch } from '@tanstack/react-router';
import { Button, Flex, Modal, Typography } from 'antd';
import { useEffect } from 'react';
import { useTimer, type TimerSettings } from 'react-timer-hook';
import useWebSocket from 'react-use-websocket';
import { getWsUrl } from '../api/game';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { chatLog, fen, gameEnded, isMyTurn, possibleMoves, winner } from '../hooks/gamestate';
import type { wsMessage } from '../types';
import { createExpireTime, parseTimings } from '../utils/time';
import { Chat } from '../components/Chat';

export const Game = () => {
    const { gameId } = useParams({ from: '/game/$gameId' as const });
    const { boardOrientation, bot } = useSearch({ from: '/game/$gameId' as const });
    const navigate = useNavigate({ from: '/game/$gameId' as const });
    const { token } = useTokenContext();
    if (!token) throw new Error('Token not found');

    const { sendJsonMessage } = useWebSocket<wsMessage>(getWsUrl(gameId), {
        queryParams: {
            token,
        },
        onMessage: (event) => {
            const message = JSON.parse(event.data) as wsMessage;

            if (message && 'waiting' in message && opponentTimer.totalSeconds <= 0) {
                // è un messaggio di tipo waiting
                // se il timer dell'avversario è scaduto, allora la partita è finita
                gameEnded.value = true;
                winner.value = true;
            }

            if (message && !('waiting' in message)) {
                // è un messaggio di tipo gamestate

                // turn handling
                isMyTurn.value = message.turn === boardOrientation;
                // updating fen
                fen.value = message.view;
                // updating gameEnded, when it's over never change it
                if (!gameEnded.value) gameEnded.value = message.ended;

                // updating winner
                if (gameEnded.value) winner.value = message.turn !== boardOrientation;

                if (message.possible_moves !== null) possibleMoves.value = message.possible_moves;
                else possibleMoves.value = [];

                // updating chat log
                chatLog.value = message.message;

                /*
                    timer handling

                    Se i timer start sono entrambi null, allora è la prima mossa della partita
                    e devo inizializzare i timer con il time left

                    Se uno dei due è null, allora devo metterlo in pausa senza variare il tempo
                    mentre quello non null deve essere aggiornato e fatto partire
                */
                if (message.using_timer) {
                    const { myTimeStart, opponentTimeStart, myTimeLeft, opponentTimeLeft } = parseTimings(
                        boardOrientation,
                        message,
                    );
                    if (myTimeStart === null && opponentTimeStart === null) {
                        const myNewTimestamp = createExpireTime(null, myTimeLeft);
                        myTimer.restart(myNewTimestamp, false);

                        const opponentNewTimestamp = createExpireTime(null, opponentTimeLeft);
                        opponentTimer.restart(opponentNewTimestamp, false);
                    } else if (myTimeStart === null) {
                        myTimer.restart(createExpireTime(null, myTimeLeft));
                        myTimer.pause();
                        opponentTimer.restart(createExpireTime(null, opponentTimeLeft));
                    } else if (opponentTimeStart === null) {
                        opponentTimer.restart(createExpireTime(null, opponentTimeLeft));
                        opponentTimer.pause();
                        myTimer.restart(createExpireTime(null, myTimeLeft));
                    }
                }
            }
        },
    });

    useEffect(() => {
        isMyTurn.value = boardOrientation === 'white';
        gameEnded.value = false;
        fen.value = boardOrientation === 'white' ? startWhiteFEN : startBlackFEN;
        possibleMoves.value = [];
        sendJsonMessage({ kind: 'list_move', data: '' });
        // sendJsonMessage is a function, not needed as a dependency
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [boardOrientation]);

    const endTimeCallback = () => {
        // Deve essere fatta una richiesta per triggerare l'endgame
        makeMove('a1', 'a1'); // mossa arbitraria a caso, utilizzata per ricevere la risposta e finire il gioco
    };

    // set the timer to 0 seconds, will be updated by the first message
    const timerSettings: TimerSettings = { expiryTimestamp: new Date(), autoStart: false, onExpire: endTimeCallback };
    const myTimer = useTimer(timerSettings);
    const opponentTimer = useTimer(timerSettings);

    const myTimeOverString = myTimer.totalSeconds <= 0 ? 'Hai finito il tempo!' : '';
    const opponentTimeOverString = opponentTimer.totalSeconds <= 0 ? "L'avversario ha finito il tempo!" : '';

    const makeMove = (from: string, to: string) => {
        if (isMyTurn.value) {
            // if i want the most update information, i need to ask the moves list AFTER making a move
            sendJsonMessage({ kind: 'move', data: `${from}${to}` });
            sendJsonMessage({ kind: 'list_move', data: '' });
        }
        // l'aggiornamento del turno è fatto dall'effect
    };

    const setUpNewGame = () => {
        gameEnded.value = false;
        navigate({ to: '/game', search: { bot: true } });
    };

    return (
        <Flex wrap="wrap" gap="large" align="center" justify="space-around">
            <Flex vertical gap="small">
                <Typography.Title level={3} type={isMyTurn.value ? 'success' : 'danger'}>
                    {isMyTurn.value ? 'È il tuo turno' : "È il turno dell'avversario"}
                </Typography.Title>
                <PlayerInfo
                    myTurn={!isMyTurn.value}
                    time={{
                        seconds: opponentTimer.seconds,
                        minutes: opponentTimer.minutes,
                        hours: opponentTimer.hours,
                        days: opponentTimer.days,
                    }}
                    opponent
                />
                <Chessboard
                    fen={fen.value}
                    boardOrientation={boardOrientation}
                    makeMove={makeMove}
                    possibleMoves={possibleMoves.value}
                />
                <PlayerInfo
                    myTurn={isMyTurn.value}
                    time={{
                        seconds: myTimer.seconds,
                        minutes: myTimer.minutes,
                        hours: myTimer.hours,
                        days: myTimer.days,
                    }}
                />
            </Flex>

            <Flex vertical gap="small" style={{ minWidth: '300px', maxWidth: '35%' }}>
                {!bot && (
                    <section>
                        <Typography.Paragraph
                            copyable={{
                                text: gameId,
                            }}
                        >
                            Se giochi con una altra persona, condividi l'ID {gameId}!
                        </Typography.Paragraph>
                        <Flex gap="small">
                            <Typography.Paragraph>Oppure postalo sui social!</Typography.Paragraph>
                            <TwitterShareButton gameId={gameId} />
                        </Flex>
                    </section>
                )}
                <Chat messages={chatLog.value} />
            </Flex>

            {/* Modal to show when game ends */}
            <Modal
                title={winner.value ? `Hai vinto! ${opponentTimeOverString} 🙂` : `Hai perso! ${myTimeOverString} ☹️`}
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

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../????????/????????/????????/????????';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
// ^ white fen is '????????/????????/????????/????????/......../......../PPPPPPPP/RNBQKBNR';
