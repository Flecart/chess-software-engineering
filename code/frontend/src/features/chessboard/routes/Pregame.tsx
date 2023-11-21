import { useTokenContext } from '@/lib/tokenContext';
import { indexGameRouteId } from '@/routes/game';
import { useNavigate, useSearch } from '@tanstack/react-router';
import { Button, Divider, Flex, Typography } from 'antd';
import Search from 'antd/es/input/Search';
import * as gameApi from '../api/game';
import { createCode, parseCode } from '../utils/code';

export const Pregame = () => {
    const navigate = useNavigate({ from: '/game' });
    const { token, setToken } = useTokenContext();
    const { bot } = useSearch({ from: indexGameRouteId });

    const checkAndSetToken = async (): Promise<string> => {
        if (!token) {
            // Permettiamo di giocare come guest
            const guestToken = await gameApi.loginAsGuest();
            setToken(guestToken);

            return guestToken;
        }

        return token;
    };

    const startGame = async () => {
        const sureToken = await checkAndSetToken();
        const realGameId = await gameApi.createGame(sureToken, bot);
        await gameApi.joinGame(sureToken, realGameId);

        navigate({
            to: '/game/$gameId',
            params: { gameId: createCode(realGameId) },
            search: { boardOrientation: 'white' },
        });
    };

    return (
        <Flex wrap="wrap">
            <section style={{ width: '25%' }}>
                <Typography.Paragraph>Scegli il tempo (To implement)</Typography.Paragraph>
                <Button onClick={startGame}>Start Game</Button>
            </section>

            <Divider orientation="left">Or</Divider>
            <section>
                <Search
                    placeholder="input game id"
                    allowClear
                    enterButton="Join Game"
                    size="large"
                    onSearch={async (gameId) => {
                        const sureToken = await checkAndSetToken();
                        await gameApi.joinGame(sureToken, parseCode(gameId));

                        navigate({
                            to: '/game/$gameId',
                            params: { gameId: gameId },
                            search: { boardOrientation: 'black' },
                        });
                    }}
                />
            </section>
        </Flex>
    );
};
