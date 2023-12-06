import { useAuth } from '@/features/auth';
import { useUserQuery } from '@/features/user';
import { ClockCircleOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, Flex } from 'antd';
import { displayTimer } from '../utils/time';
import { useMemo } from 'react';

type Props = Readonly<{
    myTurn: boolean;
    opponent?: boolean;
    time?: {
        seconds: number;
        minutes: number;
        hours: number;
        days: number;
    };
    givenUsername?: string;
}>;

// NOTA: per ragioni di refactorabilità sarebbe meglio usare un componente in stile funzionale
// ossia che non abbia dipendenze esterne come l'uso di Hooks.
// però va bene anche così, la priorità è che funzioni.
export const PlayerInfo = ({ myTurn, opponent, time, givenUsername }: Props) => {
    const { isGuest, username: myUsername } = useAuth();
    const username = givenUsername ?? (opponent ? 'Avversario' : myUsername);

    const { seconds, minutes, hours, days } = useMemo(() => {
        if (!time) return { seconds: 0, minutes: 0, hours: 0, days: 0 };
        return time;
    }, []);

    const { data: user } = useUserQuery(username, !isGuest && !opponent);
    return (
        <Flex
            align="center"
            justify="space-between"
            gap="small"
            style={{
                flexDirection: opponent ? 'row-reverse' : 'row',
                opacity: myTurn ? '1' : '.3',
            }}
        >
            <Flex align="center" gap="small">
                <Avatar shape="square" src={user?.avatar} icon={<UserOutlined />} size={'large'} />
                <span style={{ fontSize: '1.5rem' }}>{username}</span>
            </Flex>
            <Flex
                gap="small"
                style={{
                    border: '1px solid',
                    borderRadius: '3px',
                    padding: '.4rem',
                    fontWeight: 'bold',
                    background: '#f1f1f1',
                    fontSize: '1.5rem',
                }}
            >
                { time && 
                <>
                    <ClockCircleOutlined />
                    <span>{displayTimer(days, hours, minutes, seconds)}</span>
                </>
                }
            </Flex>
        </Flex>
    );
};
