import { useNavigate } from '@tanstack/react-router';
import { Button, Flex, Modal, Select } from 'antd';
import { isAxiosError } from 'axios';
import { useCallback, useEffect, useState } from 'react';
import { makeBotMove, poll, startDarkboard } from '../api/game';
import { Chat } from '../components/Chat';
import { PlayerInfo } from '../components/PlayerInfo';
import { StaticChessboard } from '../components/StaticChessboard';
import { isMyTurn } from '../hooks/gamestate';

const startFEN = 'rnbqkbnr/pppppppp/......../......../......../......../PPPPPPPP/RNBQKBNR';

export const Darkboard = () => {
    const navigate = useNavigate();

    const [isAskingForMove, setIsAskingForMove] = useState(false);
    const [hasGameStarted, setHasGameStarted] = useState(false);
    const [modalOpen, setModalOpen] = useState(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [messages, setMessages] = useState<string[]>([]);
    const [view, setView] = useState<'openspiel' | 'darkboard' | 'full'>('full');
    const [currentFen, setCurrentFen] = useState<string>(startFEN);

    const handleNewMove = useCallback(() => {
        setIsAskingForMove(true);
        makeBotMove();
    }, []);

    const handleViewSelect = useCallback((value: 'openspiel' | 'darkboard' | 'full') => {
        setView(value);
    }, []);

    useEffect(() => {
        setCurrentFen(startFEN);
        startDarkboard().then(() => {
            setHasGameStarted(true);
        });
    }, []);

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const data = await poll();
                if (data.fen != currentFen) {
                    setIsAskingForMove(false);
                    setCurrentFen(data.fen);
                }
                setErrorMessage(data.error_message ?? null);
                setMessages(data.message ?? []);

                if (data.state == 'game_over' || data.error_message != null) {
                    setModalOpen(true);
                }
            } catch (e) {
                if (isAxiosError(e)) setErrorMessage(e.response?.data as string);
                else if (e instanceof Error) setErrorMessage(e.message);
                else setErrorMessage('Errore sconosciuto');
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [hasGameStarted, currentFen]);

    return (
        <Flex wrap="wrap" gap="large" align="center" justify="space-around">
            <Flex vertical gap="small" style={{ marginTop: '4rem' }}>
                <PlayerInfo myTurn={!isMyTurn.value} givenUsername="Darkboard" opponent />
                <StaticChessboard
                    customFEN={fenCalculator(view, currentFen)}
                    style={{ width: 'max(70vw, 250px)', maxWidth: '70vh' }}
                />
                <PlayerInfo myTurn={isMyTurn.value} givenUsername="OpenSpiel" />

                <Flex gap="small" justify="space-between" align="center">
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
                        style={{ width: '12rem' }}
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
                title={'La partità è finita!'}
                open={modalOpen || errorMessage != null}
                centered
                footer={[
                    <Button key="backToHome" onClick={() => navigate({ to: '/' })}>
                        Torna alla home
                    </Button>,
                ]}
                onCancel={() => navigate({ to: '/' })}
            >
                <p>Speriamo che la partita fra i due bot sia stato di gradimento!</p>
                {errorMessage == null ? null : <p>Error: {errorMessage}</p>}
            </Modal>
        </Flex>
    );
};

function showOnlyAColor(fen: string, color: string | undefined) {
    if (color === 'white') {
        return fen.replace(/[a-z]/g, '.');
    } else if (color === 'black') {
        return fen.replace(/[A-Z]/g, '.');
    }

    return fen;
}

const fenCalculator = (view: string, currentFen: string) => {
    if (view === 'darkboard') {
        return showOnlyAColor(currentFen, 'black');
    } else if (view === 'openspiel') {
        return showOnlyAColor(currentFen, 'white');
    } else {
        return currentFen;
    }
};
