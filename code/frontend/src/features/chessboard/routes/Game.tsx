import { Button } from 'antd';
import { Chessboard } from '../components/Chessboard';
import { useNavigate } from '@tanstack/react-router';
import { startGame } from '../api/game';

type Props = {
    useParams: () => { gameId?: string };
};

export const Game = ({ useParams }: Props) => {
    const { gameId } = useParams();
    const navigate = useNavigate({ from: '/game' });
    const gameStarted = !!gameId;

    return (
        <>
            <div>{String(gameStarted)}</div>
            <Button
                disabled={gameStarted}
                onClick={async () => {
                    const res = await startGame();
                    navigate({ to: '/game/$gameId', params: { gameId: res['game-id'] } });
                }}
            >
                Start Game
            </Button>
            {/* TODO: print url */}
            <Chessboard gameId={gameId ?? ''} />
            {/* TODO: gameId as option is a bit sus */}
        </>
    );
};
