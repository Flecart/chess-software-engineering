import { useTokenContext } from '@/lib/tokenContext';
import { specificGameRouteId } from '@/routes/game';
import { useNavigate, useParams, useSearch } from '@tanstack/react-router';
import { Button, Flex, Modal, Typography } from 'antd';
import { useEffect } from 'react';
import useWebSocket from 'react-use-websocket';
import { getWsUrl } from '../api/game';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { fen, gameEnded, isMyTurn } from '../hooks/gamestate';
import type { wsMessage } from '../types';

import { useTimer, type TimerSettings } from 'react-timer-hook';
import { createExpireTime } from '../utils/time';

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
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';
    const { sendJsonMessage } = useWebSocket<wsMessage>(getWsUrl(gameId), {
        queryParams: {
            token,
        },
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
                console.log('timerozzo');
                // calcolo il nuovo timestamp di scadenza facendo time_start + time_left
                // se time start è null allora uso il timestamp attuale
                if (boardOrientation === message.turn) {
                    const myNewTimestamp = createExpireTime(
                        message.time_start_white,
                        message.time_left_white ?? '0:0:0',
                    );
                    myTimer.restart(myNewTimestamp);
                    opponentTimer.pause();
                } else {
                    const opponentNewTimestamp = createExpireTime(
                        message.time_start_black,
                        message.time_left_black ?? '0:0:0',
                    );
                    console.log('opponent new timestamp', opponentNewTimestamp.getSeconds());
                    opponentTimer.restart(opponentNewTimestamp);
                    myTimer.pause();
                }

                if (message.ended) {
                    gameEnded.value = true;
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
        console.log('enttime callback');
        // Deve essere fatta una richiesta per triggerare l'endgame
        makeMove('a1', 'a1'); // mossa arbitraria a caso, utilizzata per ricevere la risposta e finire il gioco
    };

    // SET THE TIMER TO 0 SECONDS, check if right
    // could get the value from user input in pregame
    const timerSettings: TimerSettings = { expiryTimestamp: new Date(), autoStart: false, onExpire: endTimeCallback };
    const myTimer = useTimer(timerSettings);
    const opponentTimer = useTimer(timerSettings);

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
                    gameIsEnded={gameIsEnded}
                />
                <PlayerInfo
                    color={boardOrientation}
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
