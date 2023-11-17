import { Icon } from '@/components/Icon';
import { Avatar, Flex, Typography } from 'antd';
import BronzeMedal from '/bronze_medal.png';
import GoldMedal from '/gold_medal.png';
import SilverMedal from '/silver_medal.png';

type Props = Readonly<{
    user: {
        username: string;
        elo: number;
        avatar: string;
        wins: number;
        losses: number;
        draws: number;
    };
    first?: boolean;
    second?: boolean;
    third?: boolean;
}>;

export const Usercard = ({ user, first, second, third }: Props) => {
    return (
        <Flex
            style={{
                padding: '20px',
                backgroundColor: '#DFDFDF',
                border: '1px solid black',
                borderRadius: '8px',
            }}
            gap="10px"
        >
            <Flex align="center">
                {first && <Icon icon={GoldMedal} alt="Gold Medal Icon" />}
                {second && <Icon icon={SilverMedal} alt="Silver Medal Icon" />}
                {third && <Icon icon={BronzeMedal} alt="Bronze Medal Icon" />}
                <Avatar src={user.avatar} alt="avatar" size={100} />
            </Flex>

            <Flex justify="center" align="center" vertical>
                <Typography.Text>{user.username}</Typography.Text>
                <Typography.Text>{user.elo}</Typography.Text>
            </Flex>
            <div style={{ flexGrow: '1' }}></div>
            <Flex justify="center" align="center" vertical>
                <Typography.Text>Vittorie: {user.wins}</Typography.Text>
                <Typography.Text>Sconfitte: {user.losses}</Typography.Text>
                <Typography.Text>Pareggi: {user.draws}</Typography.Text>
            </Flex>
        </Flex>
    );
};
