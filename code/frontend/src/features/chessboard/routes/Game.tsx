import { Button } from 'antd';
import { Chessboard } from '../components/Chessboard';
import { Link, useNavigate } from '@tanstack/react-router';
import { startGame } from '../api/game';
import { frontendUrl } from '@/config';

type Props = {
    useParams: () => { gameId?: string };
    useSearch: () => { boardOrientation?: 'white' | 'black' };
};

export const Game = ({ useParams, useSearch }: Props) => {
    const { gameId } = useParams();
    const { boardOrientation } = useSearch();
    const navigate = useNavigate({ from: '/game' });
    const gameStarted = !!gameId && !!boardOrientation;
    const opponentBoardOrientation = boardOrientation === 'white' ? 'black' : 'white';

    return (
        <>
            <h1>Game started: {String(gameStarted)}</h1>
            <Button
                disabled={gameStarted}
                onClick={async () => {
                    const res = await startGame();
                    navigate({
                        to: '/game/$gameId',
                        params: { gameId: res['game-id'] },
                        search: { boardOrientation: 'white' },
                    });
                }}
            >
                Start Game
            </Button>

            {gameStarted && (
                <Link to="/game/$gameId" params={{ gameId }} search={{ boardOrientation: opponentBoardOrientation }}>
                    {frontendUrl}/game/{gameId}?boardOrientation=
                    {opponentBoardOrientation}
                </Link>
            )}
            {gameStarted && <Chessboard gameId={gameId} boardOrientation={boardOrientation} />}
        </>
    );
};
