import { Link } from '@tanstack/react-router';
import { Avatar, Card, Flex, Typography } from 'antd';
import type { GameResult } from '../types';

type Props = Readonly<{
    game: GameResult;
    size?: 'small' | 'large';
}>;

export const GameCard = ({ game, size = 'large' }: Props) => {
    const gameResult = game.result === 'win' ? 'Vittoria' : 'Sconfitta';
    const gameResultColor = game.eloGain > 0 ? 'success' : 'danger';
    const eloGain = game.eloGain > 0 ? `+${game.eloGain}` : game.eloGain;
    const avatarSize = size === 'large' ? 100 : 50;
    return (
        <Card hoverable bordered>
            <Flex wrap="wrap" justify="center" align="center" gap="small">
                <Link to="/profile/$username" params={{ username: game.opponentName }}>
                    <Avatar src={game.opponentAvatar} size={avatarSize} />
                </Link>
                <Link to="/profile/$username" params={{ username: game.opponentName }}>
                    <Typography.Title level={3} style={{ margin: '0' }}>
                        {game.opponentName}
                    </Typography.Title>
                    <Typography.Text>{game.opponentElo}</Typography.Text>
                </Link>
                <div style={{ flexGrow: 1, minWidth: '2rem' }}></div>
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
