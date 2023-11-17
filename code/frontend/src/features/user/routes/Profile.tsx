import { Avatar, Typography, Flex } from 'antd';
import { GameCard } from '../components/GameCard';

export const Profile = () => {
    return (
        <>
            <Flex vertical align="center">
                <Avatar src={user.avatar} size={150} />
                <Typography.Title level={1} style={{ textAlign: 'center' }}>
                    {user.username}
                </Typography.Title>
                <Flex align="center" justify="space-evenly" wrap="wrap" style={{ width: '100%' }}>
                    <Typography.Text>Punteggio Elo: {user.eloScore}</Typography.Text>
                    <Typography.Text>Partite vinte: {user.wonGames}</Typography.Text>
                    <Typography.Text>Partite perse: {user.lostGames}</Typography.Text>
                </Flex>
            </Flex>

            <Flex gap="20px" vertical style={{ marginBottom: '20px' }}>
                <Typography.Title level={2}>Partite Recenti</Typography.Title>
                {games.map((game) => (
                    <GameCard game={game} key={game.id} />
                ))}
            </Flex>
        </>
    );
};

// TODO: use real data
const user = {
    username: 'Magnus Carlsen',
    eloScore: 1000,
    wonGames: 6,
    lostGames: 4,
    avatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
};

// TODO: use real data
const games = [
    {
        opponentName: 'Player1',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 1500,
        result: 'win',
        eloGain: 10,
        id: '1',
    },
    {
        opponentName: 'Player2',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 1600,
        result: 'loss',
        eloGain: -10,
        id: '2',
    },
    {
        opponentName: 'Player3',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 1700,
        result: 'win',
        eloGain: 15,
        id: '3',
    },
    {
        opponentName: 'Player4',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 1800,
        result: 'loss',
        eloGain: -15,
        id: '4',
    },
    {
        opponentName: 'Player5',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 1900,
        result: 'win',
        eloGain: 20,
        id: '5',
    },
    {
        opponentName: 'Player6',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 2000,
        result: 'win',
        eloGain: 25,
        id: '6',
    },
    {
        opponentName: 'Player7',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 2100,
        result: 'loss',
        eloGain: -20,
        id: '7',
    },
    {
        opponentName: 'Player8',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 2200,
        result: 'win',
        eloGain: 30,
        id: '8',
    },
    {
        opponentName: 'Player9',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 2300,
        result: 'loss',
        eloGain: -25,
        id: '9',
    },
    {
        opponentName: 'Player10',
        opponentAvatar: `https://api.dicebear.com/7.x/lorelei/svg?seed=${Math.random()}`,
        opponentElo: 2400,
        result: 'win',
        eloGain: 35,
        id: '10',
    },
];
