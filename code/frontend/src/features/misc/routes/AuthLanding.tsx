import { GameCard } from '@/features/user';
import { useUserGamesQuery, useUserQuery } from '@/features/user/';
import { Link, useNavigate } from '@tanstack/react-router';
import { Avatar, Button, Flex, Typography } from 'antd';

export const AuthLanding = () => {
    const navigate = useNavigate({ from: '/' });
    const username = 'magnus';
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
            <Flex vertical>
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
                    style={{
                        padding: '10px',
                        border: '1px solid #ddd',
                        borderRadius: '5px',
                        backgroundColor: '#fff',
                    }}
                >
                    {games.map((game) => (
                        <GameCard key={game.id} game={game} />
                    ))}
                </Flex>
            </Flex>
            <Flex justify="center" gap={100} wrap="wrap" style={{ width: '100%', marginTop: '120px' }}>
                <Button
                    type="primary"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/404' });
                    }}
                >
                    Gioca contro il computer
                </Button>
                <Button
                    type="default"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game' });
                    }}
                >
                    Gioca Online
                </Button>
            </Flex>
        </Flex>
    );
};
