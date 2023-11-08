import { Avatar, Flex } from 'antd';
import { UserOutlined } from '@ant-design/icons';

type Props = {
    color: 'white' | 'black';
    myTurn: boolean;
    opponent?: boolean;
};

export const PlayerInfo = ({ color, myTurn, opponent }: Props) => {
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
            <div style={{ border: '1px solid', borderRadius: '3px', padding: '3px' }}>Timer</div>
        </Flex>
    );
};