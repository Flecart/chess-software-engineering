import type { CustomSquareStyles } from 'react-chessboard/dist/chessboard/types';
import { describe, expect, it } from 'vitest';
import {
    generateFogObject,
    generateOldFogFen,
    generateStandardFen,
    getPieceAtSquare,
    isSquareOccupiedByColor,
} from '../fen';

const compareFen = (customFen: string, expectedFen: string) => () => {
    const result = generateStandardFen(customFen);
    expect(result).toEqual(expectedFen);
};

describe('generateStandardFen', () => {
    it(
        'should generate a standard FEN string from a already standard FEN string',
        compareFen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'),
    );

    it(
        'should handle "?" and the "." characters in the custom FEN string',
        compareFen(
            '????.???/????????/......../......../......../......../PPPPPPPP/RNBQKBNR',
            '8/8/8/8/8/8/PPPPPPPP/RNBQKBNR',
        ),
    );

    it(
        'should handle spaces as numbers in the custom FEN string',
        compareFen('rnbqkbnr/????????/8/8/8/3P4/PPP1PPPP/RNBQKBNR', 'rnbqkbnr/8/8/8/8/3P4/PPP1PPPP/RNBQKBNR'),
    );

    it(
        'should handle a string with the last row empty in the custom FEN string',
        compareFen(
            '????.???/????????/......../......../......../PPPPPPPP/RNBQKBNR/........',
            '8/8/8/8/8/PPPPPPPP/RNBQKBNR/8',
        ),
    );

    it(
        'should handle a string with . mixed with ? and numbers in the custom FEN string',
        compareFen(
            '??????.?/??n???.?/??.p1p2/??3P.?/pp1PNB2/3?.?.P/PP5Q/K1R3R1',
            '8/2n5/3p1p2/5P2/pp1PNB2/7P/PP5Q/K1R3R1',
        ),
    );
});

const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;

describe('generateFogObject', () => {
    it('should generate a correct fog object when the board is full fog', () => {
        const customFen = '????????/????????/????????/????????/????????/????????/????????/????????';
        // generate the fog object with a loop
        const expectedFogObject: { [key: string]: React.CSSProperties } = {};
        for (let i = 1; i <= 8; i++) {
            for (const label of labels) {
                const key = `${label}${i}`;
                expectedFogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' };
            }
        }

        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });

    it('should generate an empty fog object when there are no "?" characters in the custom FEN string', () => {
        const customFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const expectedFogObject = {};
        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });

    it('should generate a fog object when there are numbers representing spaces in the custom FEN string', () => {
        const customFen = 'rnbqkbnr/pppppppp/8/8/????????/????????/????????/????????';
        const expectedFogObject: { [key: string]: React.CSSProperties } = {};
        for (let i = 1; i <= 4; i++) {
            for (const label of labels) {
                const key = `${label}${i}`;
                expectedFogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' };
            }
        }
        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });

    it("should generate a fog object when there are number and '?' characters mixed in the custom FEN string", () => {
        const customFen = generateOldFogFen('????????/????????/????????/????????/4?3/4P3/PPPP1PPP/RNBQKBNR b Q - 0 16');

        const expectedFogObject: { [key: string]: React.CSSProperties } = {};

        for (let i = 5; i <= 8; i++) {
            for (const label of labels) {
                const key = `${label}${i}`;
                expectedFogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' };
            }
        }
        expectedFogObject['e4'] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' };

        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });

    it('should generate a correct fog object with a the white starting position custom FEN', () => {
        const customFen = '????????/????????/????????/????????/......../......../PPPPPPPP/RNBQKBNR';
        const expectedFogObject: { [key: string]: React.CSSProperties } = {};
        for (let i = 5; i <= 8; i++) {
            for (const label of labels) {
                const key = `${label}${i}`;
                expectedFogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' };
            }
        }
        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });

    it('should generate a correct fog object using an advanced game position custom FEN string', () => {
        const customFen = '??????.?/??n???.?/??.p1p2/??...P.?/pp1PNB2/...?.?.P/PP5Q/K1R3R1';
        const expectedFogObject: CustomSquareStyles = {
            a8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            b8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            c8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            d8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            e8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            f8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            h8: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            a7: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            b7: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            d7: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            e7: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            f7: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            h7: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            a6: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            b6: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            a5: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            b5: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            h5: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            d3: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
            f3: { backgroundColor: 'rgba(21, 21, 21, 0.95)' },
        };
        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });
});

describe('getPieceAtSquare', () => {
    it('should return null if the square is not occupied', () => {
        const fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const square = 'e4';
        const result = getPieceAtSquare(fen, square);
        expect(result).toBeNull();
    });

    it('should return the correct piece if the square is occupied by a white piece', () => {
        const fen = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR';
        const square = 'd3';
        const result = getPieceAtSquare(fen, square);
        expect(result).toEqual('wP');
    });

    it('should return the correct piece if the square is occupied by a black piece', () => {
        const fen = 'rnbqkbnr/ppp1pppp/3p4/8/8/8/PPPPPPPP/RNBQKBNR';
        const square = 'd6';
        const result = getPieceAtSquare(fen, square);
        expect(result).toEqual('bP');
    });

    it('should handle squares on the edge of the board', () => {
        const fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const square = 'h1';
        const result = getPieceAtSquare(fen, square);
        expect(result).toEqual('wR');
    });

    it('should handle squares with fog', () => {
        const fen = '????????/????????/????????/????????/8/8/PPPPPPPP/RNBQKBNR';
        const square = 'e8';
        const result = getPieceAtSquare(fen, square);
        expect(result).toBeNull();
    });
});

describe('isSquareOccupiedByColor', () => {
    it('should return false if the square is not occupied', () => {
        const fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const square = 'e4';
        const color = 'white';
        const result = isSquareOccupiedByColor(fen, square, color);
        expect(result).toEqual(false);
    });

    it('should return true if the square is occupied by a white piece', () => {
        const fen = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR';
        const square = 'd3';
        const color = 'white';
        const result = isSquareOccupiedByColor(fen, square, color);
        expect(result).toEqual(true);
    });

    it('should return true if the square is occupied by a black piece', () => {
        const fen = 'rnbqkbnr/ppp1pppp/3p4/8/8/8/PPPPPPPP/RNBQKBNR';
        const square = 'd6';
        const color = 'black';
        const result = isSquareOccupiedByColor(fen, square, color);
        expect(result).toEqual(true);
    });

    it('should return false if the square is occupied by a piece of the opposite color', () => {
        const fen = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR';
        const square = 'd3';
        const color = 'black';
        const result = isSquareOccupiedByColor(fen, square, color);
        expect(result).toEqual(false);
    });
});
