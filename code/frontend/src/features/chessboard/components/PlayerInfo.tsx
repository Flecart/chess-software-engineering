import { Avatar, Flex } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import Timer from './Timer';

type Props = {
    color: 'white' | 'black';
    myTurn: boolean;
    opponent?: boolean;
    timeRemaining?: number;
    timerStopping?: boolean;
    timerEndCallback?: () => void;
};

// TODO: refactorare il prop drilling con il timer, non è un buon pattern
export const PlayerInfo = ({ color, myTurn, opponent, timeRemaining, timerStopping, timerEndCallback}: Props) => {
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
            { timeRemaining && <Timer start={timeRemaining} stop={timerStopping} onZero={timerEndCallback}/> }
            {/* <div style={{ border: '1px solid', borderRadius: '3px', padding: '3px' }}>Timer</div> */}
        </Flex>
    );
};
