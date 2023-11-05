import { useEffect, useState } from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import { generateFogObject, generateStandardFen } from '../utils/fen';
import { getBoard, makeMove } from '../api/game';

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
// ^ white fen is 'XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/......../......../PPPPPPPP/RNBQKBNR';

type Props = {
    gameId: string;
    boardOrientation: 'white' | 'black';
    style?: React.CSSProperties;
};

export const Chessboard = ({ gameId, boardOrientation, style }: Props) => {
    const [fen, setFen] = useState(boardOrientation === 'white' ? startWhiteFEN : startBlackFEN);

    useEffect(() => {
        getBoard(gameId, boardOrientation).then((res) => {
            setFen(res.board.split('\n').reverse().join('/'));
        });
        const pollingBoard = setInterval(() => {
            getBoard(gameId, boardOrientation).then((res) => {
                if (res.has_enemy_moved) setFen(res.board.split('\n').reverse().join('/'));
            });
        }, 1000);
        return () => {
            clearInterval(pollingBoard);
        };
        // i just need to run this once, so i can ignore the dependency array
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div
            style={{
                width: 'max(70vw, 250px)',
                maxWidth: '70vh',
                ...style,
            }}
        >
            <ReactChessboard
                id="mainboard"
                boardOrientation={boardOrientation}
                position={generateStandardFen(fen)}
                customSquareStyles={generateFogObject(fen)}
                onPieceDrop={(from, to, piece) => {
                    if (
                        (boardOrientation === 'black' && piece.startsWith('w')) ||
                        (boardOrientation === 'white' && piece.startsWith('b'))
                    )
                        return false;
                    makeMove(gameId, `${from}${to}`).then((res) => {
                        setFen(res.board.split('\n').reverse().join('/'));
                    });
                    return true; //TODO: seems like it doesn't matter the return value, investigate
                }}
            />
        </div>
    );
};
