import { useState } from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import { generateFogObject, generateStandardFen } from '../utils/fen';
import { makeMove } from '../api/game';

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
                onPieceDrop={(from, to) => {
                    makeMove(gameId, `${from}${to}`).then((res) => {
                        setFen(res.board.split('\n').reverse().join('/'));
                    });
                    return true; //TODO: seems like it doesn't matter the return value, investigate
                }}
            />
        </div>
    );
};
