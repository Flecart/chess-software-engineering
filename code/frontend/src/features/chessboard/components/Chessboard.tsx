import { useState, useRef, useEffect } from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import { generateFogObject, generateStandardFen } from '../utils/fen';
import { makeMove } from '../api/game';

const customFEN = 'XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/8/8/PPPPPPPP/RNBQKBNR';

type Props = {
    gameId: string;
};

export const Chessboard = ({ gameId }: Props) => {
    const [fen, setFen] = useState(customFEN);
    const isMoved = useRef({ moved: false, move: '' });

    useEffect(() => {
        // call api
        async function getFen() {
            if (isMoved.current.moved) {
                const { board } = await makeMove(gameId, isMoved.current.move);
                setFen(board.split('\n').reverse().join('/'));
                isMoved.current.moved = false;
            }
        }

        getFen();
    }, [isMoved.current.moved]);

    return (
        <div
            style={{
                width: `70vw`,
                maxWidth: '70vh',
                margin: '3rem auto',
            }}
        >
            <ReactChessboard
                id="mainboard"
                position={generateStandardFen(fen)}
                customSquareStyles={generateFogObject(fen)}
                onPieceDrop={(from, to, piece) => {
                    console.log(piece, from, to);
                    isMoved.current.moved = true;
                    isMoved.current.move = `${from}${to}`;
                    return true;
                }}
            />
        </div>
    );
};
