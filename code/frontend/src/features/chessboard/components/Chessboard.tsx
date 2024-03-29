import { useRef, useState } from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import type { CustomSquareStyles, Piece, Square } from 'react-chessboard/dist/chessboard/types';
import type { color } from '../types';
import {
    generateFogObject,
    generateOldFogFen,
    generateStandardFen,
    getPieceAtSquare,
    isSquareOccupiedByColor,
} from '../utils/fen';

type Props = Readonly<{
    fen: string;
    possibleMoves: string[];
    boardOrientation: color;
    makeMove: (from: string, to: string) => void;
    style?: React.CSSProperties;
}>;

export const Chessboard = ({ fen, possibleMoves, boardOrientation, style, makeMove }: Props) => {
    const [lastMove, setLastMove] = useState<string[] | undefined>(undefined);
    const [moveSquares, setMoveSquares] = useState<CustomSquareStyles>({});
    const [moveFrom, setMoveFrom] = useState('');
    const [showPromotionDialog, setShowPromotionDialog] = useState(false);
    const promotionSquare = useRef<Square | undefined>(undefined);

    const drawMoves = (startingSquare: Square, moves: Square[]) => {
        const opponentColor = boardOrientation === 'black' ? 'white' : 'black';
        const newMoveSquare = {
            [startingSquare]: {
                background: 'rgba(255, 255, 0, 0.4)',
            },
            ...moves.reduce(
                (acc, move) => ({
                    ...acc,
                    [move]: {
                        background: isSquareOccupiedByColor(fen, move, opponentColor)
                            ? 'radial-gradient(circle, transparent 60%, rgba(0, 0, 0, 0.2) 25%)'
                            : 'radial-gradient(circle, rgba(0,0,0,.2) 25%, transparent 25%)',
                        borderRadius: '50%',
                    },
                }),
                {},
            ),
        };

        setMoveSquares(newMoveSquare);
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
                customSquareStyles={{ ...generateFogObject(generateOldFogFen(fen)), ...moveSquares }}
                showPromotionDialog={showPromotionDialog}
                promotionToSquare={promotionSquare.current}
                onPieceDrop={(from, to, piece) => {
                    if (movedOpponentPiece(boardOrientation, piece)) return false;

                    makeMove(from, to);
                    return true;
                }}
                onPromotionPieceSelect={(piece) => {
                    if (piece && lastMove) {
                        makeMove(`${lastMove[0]}`, `${lastMove[1]}${piece[1]?.toLowerCase()}`);
                    }
                    setShowPromotionDialog(false);
                    setMoveFrom('');
                    setMoveSquares({});
                    return true;
                }}
                onPromotionCheck={(source, target, piece) => {
                    if (movedOpponentPiece(boardOrientation, piece)) return false;

                    setLastMove([source, target]);
                    return isPromotion(source, target, piece);
                }}
                onSquareClick={(square) => {
                    const possibleMovesFromSquare = possibleMoves.filter((move) => move.startsWith(square));

                    const hasMoveOptions = possibleMovesFromSquare.length > 0;

                    if (!moveFrom) {
                        if (hasMoveOptions) {
                            setMoveFrom(square);
                            drawMoves(
                                square,
                                possibleMovesFromSquare.map((move) => move.slice(2, 4) as Square),
                            );
                        } else setMoveSquares({});
                        return;
                    }

                    if (possibleMoves.some((move) => move.startsWith(`${moveFrom}${square}`))) {
                        setLastMove([moveFrom, square]);

                        if (
                            isPromotion(moveFrom as Square, square, getPieceAtSquare(fen, moveFrom as Square) ?? 'bB')
                        ) {
                            promotionSquare.current = square;
                            setShowPromotionDialog(true);
                            return;
                        }
                        setMoveFrom('');
                        setMoveSquares({});
                        makeMove(moveFrom, square);
                    } else {
                        setMoveFrom('');
                        if (hasMoveOptions) {
                            setMoveFrom(square);
                            drawMoves(
                                square,
                                possibleMovesFromSquare.map((move) => move.slice(2, 4) as Square),
                            );
                        } else setMoveSquares({});
                    }
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
