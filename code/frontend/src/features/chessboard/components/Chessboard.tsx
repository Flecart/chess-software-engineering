import { useState } from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import type { CustomSquareStyles, Piece, Square } from 'react-chessboard/dist/chessboard/types';
import type { color } from '../types';
import { generateFogObject, generateOldFogFen, generateStandardFen } from '../utils/fen';

type Props = Readonly<{
    fen: string;
    possibleMoves: string[];
    boardOrientation: color;
    makeMove: (from: string, to: string) => void;
    style?: React.CSSProperties;
}>;

export const Chessboard = ({ fen, possibleMoves, boardOrientation, style, makeMove }: Props) => {
    const [lastMove, setLastMove] = useState<string[] | undefined>(undefined);
    const [moveSquare, setMoveSquare] = useState<CustomSquareStyles>({});

    const drawMoves = (startingSquare: Square, moves: string[]) => {
        console.log('from', startingSquare);
        console.log('to', moves);

        const newMoveSquare = {
            [startingSquare]: {
                background: 'rgba(255, 255, 0, 0.4)',
            },
            ...moves.reduce(
                (acc, move) => ({
                    ...acc,
                    [move]: {
                        background: 'radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)',
                        borderRadius: '50%',
                    },
                }),
                {},
            ),
        };
        console.log(newMoveSquare);

        setMoveSquare(newMoveSquare);
    };

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
                customSquareStyles={{ ...generateFogObject(generateOldFogFen(fen)), ...moveSquare }}
                onPieceDrop={(from, to, piece) => {
                    if (movedOpponentPiece(boardOrientation, piece)) return false;

                    makeMove(from, to);
                    return true;
                }}
                onPromotionPieceSelect={(piece) => {
                    if (piece && lastMove) {
                        makeMove(`${lastMove[0]}`, `${lastMove[1]}${piece[1]?.toLowerCase()}`);
                    }
                    return true;
                }}
                onPromotionCheck={(source, target, piece) => {
                    if (movedOpponentPiece(boardOrientation, piece)) return false;

                    setLastMove([source, target]);
                    return isPromotion(source, target, piece);
                }}
                onSquareClick={(square) => {
                    // console.log(square);
                    const possibleMovesFromPieces = possibleMoves.filter((move) => move.startsWith(square));
                    // console.log(possibleMovesFromPieces);
                    if (possibleMovesFromPieces.length === 0) setMoveSquare({});
                    else
                        drawMoves(
                            square,
                            possibleMovesFromPieces.map((move) => move.slice(2)),
                        );
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

const movedOpponentPiece = (player: color, piece: Piece) => {
    return (player === 'white' && piece.startsWith('b')) || (player === 'black' && piece.startsWith('w'));
};
