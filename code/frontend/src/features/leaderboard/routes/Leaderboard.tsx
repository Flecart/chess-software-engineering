import type { User } from '@/features/user';
import { Flex, Typography } from 'antd';
import { Usercard } from '../components/UserCard';

const { Title } = Typography;
const textHeaderStyle: React.CSSProperties = { margin: '0', marginBottom: '10px' };

export const Leaderboard = () => {
    return (
        <Flex vertical gap="10px" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <Title level={1} style={{ textAlign: 'center' }}>
                Classifica
            </Title>

            <Flex style={{ padding: '0 5px', margin: '0 20px 20px', borderBottom: '2px solid #716A6A' }} align="center">
                <div style={{ width: '11%' }}></div>
                <Title level={3} style={textHeaderStyle}>
                    Utente
                </Title>
                <div style={{ width: '34%' }}></div>
                <Title level={3} style={textHeaderStyle}>
                    Vittorie
                </Title>
                <div style={{ width: '15%' }}></div>
                <Title level={3} style={textHeaderStyle}>
                    Sconfitte
                </Title>
            </Flex>

            {mockUsers.map((user, i) => (
                <Usercard key={user.username} user={user} position={i + 1} />
            ))}
        </Flex>
    );
};

const mockUsers: User[] = Array.from({ length: 10 }, (_, i) => ({
    username: `User${i + 1}`,
    elo: Math.floor(Math.random() * 2000),
    avatar: `https://api.dicebear.com/7.x/croodles/svg?seed=${i + 1}`,
    wins: Math.floor(Math.random() * 100),
    losses: Math.floor(Math.random() * 100),
}));
