import { useState } from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import type { Piece, Square } from 'react-chessboard/dist/chessboard/types';
import { generateFogObject, generateOldFogFen, generateStandardFen } from '../utils/fen';

type Props = {
    fen: string;
    boardOrientation: 'white' | 'black';
    makeMove: (from: string, to: string) => void;
    style?: React.CSSProperties;
    gameIsEnded: () => void;
};

export const Chessboard = ({ fen, boardOrientation, style, makeMove }: Props) => {
    const [lastMove, setLastMove] = useState<string[] | undefined>(undefined);
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
                onPromotionPieceSelect={(piece) => {
                    if (piece && lastMove) {
                        makeMove(`${lastMove[0]}`, `${lastMove[1]}${piece[1]?.toLowerCase()}`);
                    }
                    return true;
                }}
                onPromotionCheck={(source, target, piece) => {
                    if (
                        (boardOrientation === 'black' && piece.startsWith('w')) ||
                        (boardOrientation === 'white' && piece.startsWith('b'))
                    )
                        return false;
                    setLastMove([source, target]);
                    return isPromotion(source, target, piece);
                }}
            />
        </div>
    );
};

const isPromotion = (sourceSquare: Square, targetSquare: Square, piece: Piece) => {
    return (
        ((piece === 'wP' && sourceSquare[1] === '7' && targetSquare[1] === '8') ||
            (piece === 'bP' && sourceSquare[1] === '2' && targetSquare[1] === '1')) &&
        Math.abs(sourceSquare.charCodeAt(0) - targetSquare.charCodeAt(0)) <= 1
    );
};
