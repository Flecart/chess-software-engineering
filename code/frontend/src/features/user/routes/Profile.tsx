import { specificProfileRoute } from '@/routes/profile';
import { useParams } from '@tanstack/react-router';
import { Avatar, Flex, Typography } from 'antd';
import { GameCard } from '../components/GameCard';
import { useUserGamesQuery, useUserQuery } from '../hooks/useUser';

const bigText: React.CSSProperties = {
    fontSize: '1.1rem',
};

export const Profile = () => {
    const params = useParams({ from: specificProfileRoute.id });
    const { data: user, error: userError } = useUserQuery(params.username);
    const { data: games, error: gamesError } = useUserGamesQuery(params.username);

    return (
        <>
            {!!user && (
                <Flex vertical align="center">
                    <Avatar src={user.avatar} size={150} />
                    <Typography.Title level={1} style={{ textAlign: 'center' }}>
                        {user.username}
                    </Typography.Title>
                    <Flex align="center" justify="space-evenly" wrap="wrap" style={{ width: '100%' }}>
                        <Typography.Text style={bigText}>Punteggio Elo: {user.eloScore}</Typography.Text>
                        <Typography.Text style={bigText}>Partite vinte: {user.wonGames}</Typography.Text>
                        <Typography.Text style={bigText}>Partite perse: {user.lostGames}</Typography.Text>
                    </Flex>
                </Flex>
            )}
            {!user && !!userError && <Typography.Text type="danger">Errore: {userError.message}</Typography.Text>}
            {!user && !userError && <Typography.Text>Caricamento...</Typography.Text>}
            {!!games && (
                <Flex gap="20px" vertical style={{ maxWidth: '1000px', margin: '0 auto', marginBottom: '20px' }}>
                    <Typography.Title level={2} style={{ textAlign: 'center' }}>
                        Partite Recenti
                    </Typography.Title>
                    {games.map((game) => (
                        <GameCard game={game} key={game.id} />
                    ))}
                </Flex>
            )}
            {!games && !!gamesError && <Typography.Text type="danger">Errore: {gamesError.message}</Typography.Text>}
            {!games && !gamesError && <Typography.Text>Caricamento...</Typography.Text>}
        </>
    );
};
