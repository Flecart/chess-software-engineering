import { Link } from '@tanstack/react-router';
import { Avatar, Card, Flex, Typography } from 'antd';
import type { GameResult } from '../types';

type Props = Readonly<{
    game: GameResult;
}>;

export const GameCard = ({ game }: Props) => {
    const gameResult = game.result === 'win' ? 'Vittoria' : 'Sconfitta';
    const gameResultColor = game.eloGain > 0 ? 'success' : 'danger';
    const eloGain = game.eloGain > 0 ? `+${game.eloGain}` : game.eloGain;
    return (
        <Card hoverable bordered>
            <Flex wrap="wrap" justify="center" gap="small">
                <Link to="/profile/$username" params={{ username: game.opponentName }}>
                    <Avatar src={game.opponentAvatar} size={100} />
                </Link>
                <Link to="/profile/$username" params={{ username: game.opponentName }}>
                    <Typography.Title level={3}>{game.opponentName}</Typography.Title>
                    <Typography.Text>{game.opponentElo}</Typography.Text>
                </Link>
                <div style={{ flexGrow: 1 }}></div>
                <Flex vertical justify="space-evenly" align="center">
                    <Typography.Text type={gameResultColor} strong style={{ fontSize: '1rem' }}>
                        {gameResult} {eloGain}
                    </Typography.Text>
                    <Typography.Link href={`#${game.id}`}>Dettagli Partita</Typography.Link>
                </Flex>
            </Flex>
        </Card>
    );
};
