import { Avatar, Flex, Typography } from 'antd';

type Props = Readonly<{
    game: {
        opponentName: string;
        opponentAvatar: string;
        opponentElo: number;
        result: string;
        eloGain: number;
        id: string;
    };
}>;

export const GameCard = ({ game }: Props) => {
    const gameResult = game.result === 'win' ? 'Vittoria' : 'Sconfitta';
    const gameResultColor = game.eloGain > 0 ? 'success' : 'danger';
    return (
        <Flex
            wrap="wrap"
            justify="center"
            style={{
                border: '1px solid black',
                backgroundColor: '#DFDFDF',
                borderRadius: '8px',
                padding: '10px',
                margin: '0 30px',
            }}
        >
            <Avatar src={game.opponentAvatar} size={100} />
            <div>
                <Typography.Title level={3}>{game.opponentName}</Typography.Title>
                <Typography.Text>{game.opponentElo}</Typography.Text>
            </div>
            <div style={{ flexGrow: 1 }}></div>
            <Flex vertical justify="space-between" align="center">
                <Typography.Text type={gameResultColor}>{gameResult}</Typography.Text>
                <Typography.Text type={gameResultColor}>{game.eloGain}</Typography.Text>
                <Typography.Link href={`#${game.id}`}>Dettagli Partita</Typography.Link>
            </Flex>
        </Flex>
    );
};
