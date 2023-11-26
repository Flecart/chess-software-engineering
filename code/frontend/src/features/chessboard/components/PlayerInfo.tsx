import { ClockCircleOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, Flex } from 'antd';
import type { color } from '../types';
import { displayTimer } from '../utils/time';

type Props = {
    color: color;
    myTurn: boolean;
    opponent?: boolean;
    time: {
        seconds: number;
        minutes: number;
        hours: number;
        days: number;
    };
};

export const PlayerInfo = ({ color, myTurn, opponent, time }: Props) => {
    const { seconds, minutes, hours, days } = time;
    return (
        <Flex
            align="center"
            gap="small"
            style={{ flexDirection: opponent ? 'row-reverse' : 'row', opacity: myTurn ? '1' : '.3' }}
        >
            <Avatar shape="square" icon={<UserOutlined />} />
            <p>{color === 'black' ? 'Nero' : 'Bianco'}</p>
            {/* space filler */}
            <div style={{ width: '100%' }}></div>
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    fontSize: '2em',
                    fontWeight: 'bold',
                    color: '#333',
                    background: '#f5f5f5',
                    minWidth: '300px',
                }}
            >
                <ClockCircleOutlined /> {displayTimer(days, hours, minutes, seconds)}
            </div>
            {/* <div style={{ border: '1px solid', borderRadius: '3px', padding: '3px' }}>Timer</div> */}
        </Flex>
    );
};
