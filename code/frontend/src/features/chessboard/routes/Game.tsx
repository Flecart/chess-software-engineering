import { useTokenContext } from '@/lib/tokenContext';
import { specificGameRouteId } from '@/routes/game';
import { useNavigate, useParams, useSearch } from '@tanstack/react-router';
import { Button, Flex, Modal, Typography } from 'antd';
import { useEffect } from 'react';
import { useTimer, type TimerSettings } from 'react-timer-hook';
import useWebSocket from 'react-use-websocket';
import { getWsUrl } from '../api/game';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { fen, gameEnded, isMyTurn } from '../hooks/gamestate';
import type { wsMessage } from '../types';
import { createExpireTime } from '../utils/time';

export const Game = () => {
    const { gameId } = useParams({ from: specificGameRouteId });
    const { boardOrientation } = useSearch({ from: specificGameRouteId });
    const navigate = useNavigate({ from: specificGameRouteId });
    const { token } = useTokenContext();

    // TODO: gestire meglio questo, dovrà essere in useEffect, e l'errore mostrato (magari un redirecto?)
    if (!token) throw new Error('Token not found');
    const { sendJsonMessage } = useWebSocket<wsMessage>(getWsUrl(gameId), {
        queryParams: {
            token,
        },
        onMessage: (event) => {
            const message = JSON.parse(event.data) as wsMessage;

            if (message && 'ended' in message) {
                // è un messaggio di tipo gamestate

                // turn handling
                if (isMyTurn.value && message.move_made !== null) isMyTurn.value = false;
                else if (!isMyTurn.value) isMyTurn.value = true;

                // updating fen
                fen.value = message.view;
                // updating gameEnded
                gameEnded.value = message.ended;

                /*
                    timer handling

                    Se i timer start sono entrambi null, allora è la prima mossa della partita
                    e devo inizializzare i timer con il time left

                    Se uno dei due è null, allora devo metterlo in pausa senza variare il tempo
                    mentre quello non null deve essere aggiornato e fatto partire
                */
                const timeLeftWhite = message.time_left_white ?? '0:0:0';
                const timeLeftBlack = message.time_left_black ?? '0:0:0';

                if (message.time_start_white === null && message.time_start_black === null) {
                    const myNewTimestamp = createExpireTime(null, timeLeftWhite);
                    myTimer.restart(myNewTimestamp, false);

                    const opponentNewTimestamp = createExpireTime(null, timeLeftBlack);
                    opponentTimer.restart(opponentNewTimestamp, false);
                } else if (message.time_start_white === null) {
                    myTimer.restart(createExpireTime(null, timeLeftWhite));
                    myTimer.pause();
                    opponentTimer.restart(createExpireTime(message.time_start_black, timeLeftBlack));
                } else if (message.time_start_black === null) {
                    opponentTimer.restart(createExpireTime(null, timeLeftBlack));
                    opponentTimer.pause();
                    myTimer.restart(createExpireTime(message.time_start_white, timeLeftWhite));
                }
            }
        },
    });

    useEffect(() => {
        isMyTurn.value = boardOrientation === 'white';
        gameEnded.value = false;
        fen.value = boardOrientation === 'white' ? startWhiteFEN : startBlackFEN;
    }, [boardOrientation]);

    const endTimeCallback = () => {
        // Deve essere fatta una richiesta per triggerare l'endgame
        makeMove('a1', 'a1'); // mossa arbitraria a caso, utilizzata per ricevere la risposta e finire il gioco
    };

    // set the timer to 0 seconds, will be updated by the first message
    const timerSettings: TimerSettings = { expiryTimestamp: new Date(), autoStart: false, onExpire: endTimeCallback };
    const myTimer = useTimer(timerSettings);
    const opponentTimer = useTimer(timerSettings);

    const makeMove = (from: string, to: string) => {
        if (isMyTurn.value) sendJsonMessage({ kind: 'move', data: `${from}${to}` });
        // l'aggiornamento del turno è fatto dall'effect
    };

    const setUpNewGame = () => {
        gameEnded.value = false;
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
                    myTurn={!isMyTurn.value}
                    time={{
                        seconds: opponentTimer.seconds,
                        minutes: opponentTimer.minutes,
                        hours: opponentTimer.hours,
                        days: opponentTimer.days,
                    }}
                    opponent
                />
                <Chessboard fen={fen.value} boardOrientation={boardOrientation} makeMove={makeMove} />
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

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../????????/????????/????????/????????';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
// ^ white fen is '????????/????????/????????/????????/......../......../PPPPPPPP/RNBQKBNR';
