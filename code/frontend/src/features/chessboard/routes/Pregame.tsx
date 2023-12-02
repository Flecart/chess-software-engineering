import { useState } from 'react';
import { useTokenContext } from '@/lib/tokenContext';
import { useNavigate, useSearch } from '@tanstack/react-router';
import { Button, Divider, Flex, Form, Select, Typography } from 'antd';
import Search from 'antd/es/input/Search';
import type { DefaultOptionType } from 'antd/es/select';
import * as gameApi from '../api/game';
import type { GameOptions } from '../types';

export const Pregame = () => {
    const navigate = useNavigate({ from: '/game/' as const });
    const { token, setToken } = useTokenContext();
    const { bot, sharedGameId } = useSearch({ from: '/game/' as const });
    const [gameId, setGameId] = useState<string>(sharedGameId || '');

    const checkAndSetToken = async (): Promise<string> => {
        if (!token) {
            // Permettiamo di giocare come guest
            const guestToken = await gameApi.loginAsGuest();
            setToken(guestToken);

            return guestToken;
        }

        return token;
    };

    const startGame = async (values: GameOptions) => {
        console.log(values);
        const sureToken = await checkAndSetToken();

        const realGameId = await gameApi.createGame(sureToken, bot, values.variant, values.time);
        const color = await gameApi.joinGame(sureToken, realGameId, values.color);
        navigate({
            to: '/game/$gameId',
            params: { gameId: realGameId },
            search: { boardOrientation: color },
        });
    };

    return (
        <Flex wrap="wrap" align="center" vertical>
            <Typography.Title level={1}>{bot ? 'Partita contro il computer' : 'Partita online'}</Typography.Title>
            <Flex vertical gap="small">
                <Form
                    onFinish={startGame}
                    layout="inline"
                    name="start-game"
                    initialValues={{
                        time: 3,
                        color: colorOptions[0]?.value,
                        variant: gameVariantOptions[0]?.value,
                    }}
                >
                    <Form.Item label="Variante: " name="variant">
                        <Select bordered={false} options={gameVariantOptions} style={{ minWidth: '150px' }} />
                    </Form.Item>
                    <Form.Item label="Tempo: " name="time">
                        <Select bordered={false} options={timeOptions} style={{ minWidth: '150px' }} />
                    </Form.Item>
                    <Form.Item label="Colore: " name="color">
                        <Select bordered={false} options={colorOptions} style={{ minWidth: '100px' }} />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Nuova Partita
                        </Button>
                    </Form.Item>
                </Form>
            </Flex>
            {!bot && <Divider>Oppure</Divider>}
            {!bot && (
                <section>
                    <Search
                        value={gameId}
                        onChange={(e) => setGameId(e.target.value)}
                        placeholder="Inserisci il codice partita"
                        allowClear
                        enterButton="Unisciti"
                        onSearch={async () => {
                            const sureToken = await checkAndSetToken();
                            const color = await gameApi.joinGame(sureToken, gameId);

                            navigate({
                                to: '/game/$gameId',
                                params: { gameId: gameId },
                                search: { boardOrientation: color },
                            });
                        }}
                    />
                </section>
            )}
        </Flex>
    );
};

const gameVariantOptions: DefaultOptionType[] = [
    { label: 'Dark Chess', value: 'dark_chess' },
    { label: 'Kriegspiel', value: 'kriegspiel' },
];

const timeOptions: DefaultOptionType[] = [
    { label: 'Nessun tempo', value: 0 },
    { label: '3 minuti', value: 3 },
    { label: '5 minuti', value: 5 },
    { label: '10 minuti', value: 10 },
    { label: '30 minuti', value: 30 },
];

const colorOptions: DefaultOptionType[] = [
    { label: 'Bianco', value: 'white' },
    { label: 'Nero', value: 'black' },
];
