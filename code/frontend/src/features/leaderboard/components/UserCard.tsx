import { Icon } from '@/components/Icon';
import type { User } from '@/features/user';
import { Avatar, Card, Flex, Typography } from 'antd';
import { ArrowDownCircle, ArrowUpCircle } from 'lucide-react';
import BronzeMedal from '/bronze_medal.png';
import GoldMedal from '/gold_medal.png';
import SilverMedal from '/silver_medal.png';

type Props = Readonly<{
    user: User;
    position: number;
}>;

const bigText: React.CSSProperties = { fontSize: '16px' };
const columnStyle: React.CSSProperties = { width: '33%' };

const { Text } = Typography;

export const Usercard = ({ user, position }: Props) => {
    return (
        <Card hoverable bordered>
            <Card.Meta
                avatar={
                    <Flex align="center">
                        <div style={{ minWidth: '40px' }}>
                            {position === 1 && <Icon icon={GoldMedal} alt="Gold Medal Icon" />}
                            {position === 2 && <Icon icon={SilverMedal} alt="Silver Medal Icon" />}
                            {position === 3 && <Icon icon={BronzeMedal} alt="Bronze Medal Icon" />}
                            {position > 3 && (
                                <Text strong style={{ fontSize: '20px' }}>
                                    #{position}
                                </Text>
                            )}
                        </div>

                        <Avatar src={user.avatar} alt="avatar" size={100} />
                    </Flex>
                }
                title={<Text style={{ fontSize: '20px' }}>{user.username}</Text>}
                description={
                    <Flex justify="space-between" align="center" wrap="wrap">
                        <Text style={{ ...bigText, ...columnStyle, color: 'GrayText' }}>ELO: {user.elo}</Text>
                        <Flex align="center" justify="center" gap="4px" style={columnStyle}>
                            <ArrowUpCircle color="#009B77" />
                            <Text style={bigText}>
                                Vittorie:{' '}
                                <Text style={bigText} strong>
                                    {user.wins}
                                </Text>
                            </Text>
                        </Flex>
                        <Flex align="center" justify="center" gap="4px" style={columnStyle}>
                            <ArrowDownCircle color="#a1000e" />
                            <Text style={bigText}>
                                Sconfitte:{' '}
                                <Text style={bigText} strong>
                                    {user.losses}
                                </Text>
                            </Text>
                        </Flex>
                    </Flex>
                }
            />
        </Card>
    );
};
