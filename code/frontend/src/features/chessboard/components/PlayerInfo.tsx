import { ClockCircleOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, Flex } from 'antd';
import type { color } from '../types';
import { displayTimer } from '../utils/time';

type Props = Readonly<{
    color: color;
    myTurn: boolean;
    opponent?: boolean;
    time: {
        seconds: number;
        minutes: number;
        hours: number;
        days: number;
    };
}>;

export const PlayerInfo = ({ color, myTurn, opponent, time }: Props) => {
    const { seconds, minutes, hours, days } = time;
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
                <Avatar shape="square" icon={<UserOutlined />} size={'large'} />
                <span style={{ fontSize: '1.5rem' }}>{color === 'black' ? 'Nero' : 'Bianco'}</span>
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
                <ClockCircleOutlined />
                <span>{displayTimer(days, hours, minutes, seconds)}</span>
            </Flex>
        </Flex>
    );
};
