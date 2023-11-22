import { Flex, Typography } from 'antd';
import { Usercard } from '../components/UserCard';
import { useLeaderboardQuery } from '../hooks/useLeaderboard';

const { Title } = Typography;
const textHeaderStyle: React.CSSProperties = { margin: '0', marginBottom: '10px' };

export const Leaderboard = () => {
    const { data: leaderboard, error } = useLeaderboardQuery();

    const thereIsLeaderboard = !!leaderboard && leaderboard.length > 0;

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

            {(() => {
                if (thereIsLeaderboard)
                    return leaderboard.map((user, i) => <Usercard key={user.username} user={user} position={i + 1} />);

                if (error) return <p>Errore nel caricamento della classifica</p>;

                return <p>Caricamento...</p>;
            })()}
        </Flex>
    );
};
