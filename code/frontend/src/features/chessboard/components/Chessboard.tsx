import { Chessboard as ReactChessboard } from 'react-chessboard';
import { generateFogObject, generateOldFogFen, generateStandardFen } from '../utils/fen';

const startBlackFEN = 'rnbqkbnr/pppppppp/......../......../XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX';
const startWhiteFEN = startBlackFEN.toUpperCase().split('/').reverse().join('/');
// ^ white fen is 'XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/......../......../PPPPPPPP/RNBQKBNR';

type Props = {
    fen?: string;
    boardOrientation: 'white' | 'black';
    makeMove: (from: string, to: string) => void;
    style?: React.CSSProperties;
    gameIsEnded: () => void;
};

export const Chessboard = ({ fen, boardOrientation, style, makeMove }: Props) => {
    if (!fen) fen = boardOrientation === 'white' ? startWhiteFEN : startBlackFEN;

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
                customSquareStyles={generateFogObject(generateOldFogFen(fen))}
                onPieceDrop={(from, to, piece) => {
                    if (
                        (boardOrientation === 'black' && piece.startsWith('w')) ||
                        (boardOrientation === 'white' && piece.startsWith('b'))
                    )
                        return false;
                    makeMove(from, to);
                    return true; //TODO: seems like it doesn't matter the return value, investigate
                }}
            />
        </div>
    );
};
