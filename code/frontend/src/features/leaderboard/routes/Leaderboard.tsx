import { Flex, Typography } from 'antd';
import { Usercard } from '../components/UserCard';

export const Leaderboard = () => {
    return (
        <Flex vertical gap="10px" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <Typography.Title level={1} style={{ textAlign: 'center' }}>
                Classifica
            </Typography.Title>
            {mockUsers.map((user, i) => (
                <Usercard key={user.username} user={user} first={i === 0} second={i === 1} third={i === 2} />
            ))}
        </Flex>
    );
};

const mockUsers = Array.from({ length: 10 }, (_, i) => ({
    username: `User${i + 1}`,
    elo: Math.floor(Math.random() * 2000),
    avatar: `https://api.dicebear.com/7.x/croodles/svg?seed=${i + 1}`,
    wins: Math.floor(Math.random() * 100),
    losses: Math.floor(Math.random() * 100),
    draws: Math.floor(Math.random() * 100),
}));
