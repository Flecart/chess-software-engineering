import { useNavigate } from '@tanstack/react-router';
import { Button, Flex, Modal, Select } from 'antd';
import { useEffect, useCallback, useState } from 'react';
import { Chessboard } from '../components/Chessboard';
import { PlayerInfo } from '../components/PlayerInfo';
import { fen, gameEnded, isMyTurn, winner } from '../hooks/gamestate';
import {poll, startDarkboard, makeBotMove} from '@/features/chessboard/api/game';
import { Chat } from '../components/Chat';

export const Darkboard = () => {
    const navigate = useNavigate();

    const [isAskingForMove, setisAskingForMove] = useState(false);
    const [hasGameStarted, setHasGameStarted] = useState(false);
    const [messages, setMessages] = useState<string[]>([]);
    const [view, setView] = useState<"openspiel" | "darkboard" | "full">('full');

    const setUpNewGame = useCallback(() => {
        gameEnded.value = false;
        navigate({ to: '/game', search: { bot: true } });
    }, [navigate]);

    const handleNewMove = useCallback(() => {
        setisAskingForMove(true);
        makeBotMove();
    }, []);

    const handleViewSelect = useCallback((value: "openspiel" | "darkboard" | "full") => {
        setView(value);
    }, []);

    const fenCalculator = useCallback((currentFen: string) => {
        if (view === 'darkboard') {
            return showOnlyAColor(currentFen, 'black');
        } else if (view === 'openspiel') {
            return showOnlyAColor(currentFen, 'white');
        } else {
            return currentFen;
        }
    }, [view]);

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
            setMessages(data.message ?? []);
        }, 1000);

        return () => clearInterval(interval);
    }, [hasGameStarted]);

    return (
        <Flex wrap="wrap" gap="large" align="center" justify="space-around">
            <Flex vertical gap="small" style={{marginTop: "4rem"}}>
                <PlayerInfo
                    myTurn={!isMyTurn.value}
                    givenUsername="Darkboard"
                    opponent
                />
                <Chessboard
                    fen={fenCalculator(fen.value)}
                    boardOrientation={'white'}
                    possibleMoves={[]}
                    makeMove={() => console.log('Can´t  make move!')}
                />
                <PlayerInfo
                    myTurn={isMyTurn.value}
                    givenUsername="OpenSpiel"
                />

                <Flex gap="small" justify="space-between" align='center'>
                <Button
                    type="primary"
                    size="large"
                    style={{ maxWidth: '10rem' }}
                    onClick={() => {
                        handleNewMove();
                    }}
                    loading={isAskingForMove}
                >
                    Make Move
                </Button>
                <Select
                    defaultValue="full"
                    style={{ width: "12rem" }}
                    onChange={handleViewSelect}
                    options={[
                        { value: 'darkboard', label: 'Darkboard view' },
                        { value: 'full', label: 'Full view' },
                        { value: 'openspiel', label: 'Openspiel view' },
                    ]}
                    />
                </Flex>
            </Flex>
            <Flex vertical gap="small" style={{ minWidth: '300px', maxWidth: '35%' }}>
                <Chat messages={messages} />
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

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');

function showOnlyAColor(fen:string, color: string|undefined) {
    if (color === 'white') {
        return fen.replace(/[a-z]/g, '.')
    } else if (color === 'black'){
        return fen.replace(/[A-Z]/g, '.')
    }

    return fen
}