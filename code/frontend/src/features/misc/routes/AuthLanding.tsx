import { useUsername } from '@/features/auth';
import { GameCard } from '@/features/user';
import { useUserGamesQuery, useUserQuery } from '@/features/user/';
import { useTokenContext } from '@/lib/tokenContext';
import { Link, useNavigate } from '@tanstack/react-router';
import { Avatar, Button, Flex, Typography } from 'antd';

export const AuthLanding = () => {
    const navigate = useNavigate({ from: '/' });
    const { token } = useTokenContext();
    const username = useUsername(token);
    const { data: user } = useUserQuery(username);
    const { data } = useUserGamesQuery(username);

    // get the fist 3 games
    const games = data?.slice(0, 3) ?? [];

    return (
        <Flex vertical gap="small" wrap="wrap" style={{ margin: '50px auto 0', maxWidth: '1200px' }}>
            <Flex align="center">
                <Link to="/profile" style={{ fontSize: '20px', display: 'inline-block' }}>
                    <Avatar size="large" src={user?.avatar} />
                    {username}
                </Link>
            </Flex>
            <Flex justify="space-around" align="center">
                <Flex justify="center" vertical style={{ maxWidth: '600px' }}>
                    <Typography.Title
                        level={2}
                        style={{
                            padding: '15px',
                            border: '1px solid #ddd',
                            borderRadius: '5px',
                            backgroundColor: '#ededed',
                            boxShadow: 'rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px',
                        }}
                    >
                        Le tue partite recenti
                    </Typography.Title>
                    <Flex
                        gap="small"
                        align="center"
                        justify="center"
                        vertical
                        style={{
                            padding: '10px',
                            border: '1px solid #ddd',
                            borderRadius: '5px',
                            backgroundColor: '#fff',
                        }}
                    >
                        {games.map((game) => (
                            <GameCard key={game.id} game={game} size="small" />
                        ))}
                    </Flex>
                </Flex>
                <Flex gap="large" vertical style={{ maxWidth: '540px' }}>
                    <Typography.Title>Federazione Italiana Scacchisti Eterodossi - Check Mates</Typography.Title>
                    <Typography.Paragraph style={{ textAlign: 'justify' }}>
                        Dark chess è una variante degli scacchi con informazione incompleta, simile al Kriegspiel. È
                        stato inventato da Jens Bæk Nielsen e Torben Osted nel 1989. Un giocatore non vede l'intera
                        scacchiera - solo i propri pezzi e le caselle in cui può legalmente muoversi.
                    </Typography.Paragraph>
                </Flex>
            </Flex>
            <Flex justify="center" gap={100} wrap="wrap" style={{ width: '100%', marginTop: '120px' }}>
                <Button
                    type="primary"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game/', search: { bot: true } });
                    }}
                >
                    Gioca contro il computer
                </Button>
                <Button
                    type="default"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game/', search: { bot: false } });
                    }}
                >
                    Gioca Online
                </Button>
            </Flex>
        </Flex>
    );
};
