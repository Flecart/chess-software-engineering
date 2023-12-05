import { useNavigate } from '@tanstack/react-router';
import { Button, Flex, Modal } from 'antd';
import { useEffect, useCallback, useState } from 'react';
import { useTimer, type TimerSettings } from 'react-timer-hook';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { fen, gameEnded, isMyTurn, winner } from '../hooks/gamestate';
import {poll, startDarkboard, makeBotMove} from '@/features/chessboard/api/game';

export const Darkboard = () => {
    // const { token } = useTokenContext();
    // if (!token) throw new Error('Token not found');
    const navigate = useNavigate();

    const timerSettings: TimerSettings = { expiryTimestamp: new Date(), autoStart: false };

    const myTimer = useTimer(timerSettings);
    const opponentTimer = useTimer(timerSettings);

    const [isAskingForMove, setisAskingForMove] = useState(false);
    const [hasGameStarted, setHasGameStarted] = useState(false);

    const setUpNewGame = useCallback(() => {
        gameEnded.value = false;
        navigate({ to: '/game', search: { bot: true } });
    }, [navigate]);

    const handleNewMove = useCallback(() => {
        setisAskingForMove(true);
        makeBotMove();
    }, []);

    useEffect(() => {
        fen.value = startWhiteFEN;
        startDarkboard()
        .then(() => {
            setHasGameStarted(true);
        });
    }, []);

    useEffect(() => {
        const interval = setInterval(async () => {
            const data = await poll();
            if (data.fen != fen.value) {
                setisAskingForMove(false);
            }
            fen.value = data.fen;
        }, 1000);

        return () => clearInterval(interval);
    }, [hasGameStarted]);

    return (
        <Flex wrap="wrap">
            <Flex vertical gap="small" style={{ margin: '4rem 0 0 30%' }}>
                <PlayerInfo
                    myTurn={!isMyTurn.value}
                    time={{
                        seconds: opponentTimer.seconds,
                        minutes: opponentTimer.minutes,
                        hours: opponentTimer.hours,
                        days: opponentTimer.days,
                    }}
                    givenUsername="Darkboard"
                    opponent
                />
                <Chessboard
                    fen={fen.value}
                    boardOrientation={'white'}
                    makeMove={() => console.log('Can´t  make move!')}
                />
                <PlayerInfo
                    myTurn={isMyTurn.value}
                    time={{
                        seconds: myTimer.seconds,
                        minutes: myTimer.minutes,
                        hours: myTimer.hours,
                        days: myTimer.days,
                    }}
                    givenUsername="OpenSpiel"
                />
                <Button
                    type="primary"
                    size="large"
                    style={{ marginTop: '1rem', maxWidth: '10rem' }}
                    onClick={() => {
                        handleNewMove();
                    }}
                    loading={isAskingForMove}
                >
                    Make Move
                </Button>
            </Flex>

            {/* Modal to show when game ends */}
            <Modal
                title={winner.value ? `Hai vinto! 🙂` : `Hai perso! ☹️`}
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

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../......../......../......../........';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
