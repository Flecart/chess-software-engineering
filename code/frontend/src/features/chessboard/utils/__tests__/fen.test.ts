import { describe, expect, it } from 'vitest';
import { generateFogObject, generateStandardFen } from '../fen';
import type { CustomSquareStyles } from 'react-chessboard/dist/chessboard/types';

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
        'should handle "X" and the "." characters in the custom FEN string',
        compareFen(
            'XXXX.XXX/XXXXXXXX/......../......../......../......../PPPPPPPP/RNBQKBNR',
            '8/8/8/8/8/8/PPPPPPPP/RNBQKBNR',
        ),
    );

    it(
        'should handle spaces as numbers in the custom FEN string',
        compareFen('rnbqkbnr/XXXXXXXX/8/8/8/3P4/PPP1PPPP/RNBQKBNR', 'rnbqkbnr/8/8/8/8/3P4/PPP1PPPP/RNBQKBNR'),
    );

    it(
        'should handle a string with the last row empty in the custom FEN string',
        compareFen(
            'XXXX.XXX/XXXXXXXX/......../......../......../PPPPPPPP/RNBQKBNR/........',
            '8/8/8/8/8/PPPPPPPP/RNBQKBNR/8',
        ),
    );

    it(
        'should handle a string with . mixed with X and numbers in the custom FEN string',
        compareFen(
            'XXXXXX.X/XXnXXX.X/XX.p1p2/XX3P.X/pp1PNB2/3X.X.P/PP5Q/K1R3R1',
            '8/2n5/3p1p2/5P2/pp1PNB2/7P/PP5Q/K1R3R1',
        ),
    );
});

const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;

describe('generateFogObject', () => {
    it('should generate a correct fog object when the board is full fog', () => {
        const customFen = 'XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX';
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

    it('should generate an empty fog object when there are no "X" characters in the custom FEN string', () => {
        const customFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const expectedFogObject = {};
        const result = generateFogObject(customFen);
        expect(result).toEqual(expectedFogObject);
    });

    it('should generate a fog object when there are numbers representing spaces in the custom FEN string', () => {
        const customFen = 'rnbqkbnr/pppppppp/8/8/XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX';
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

    it('should generate a correct fog object with a the white starting position custom FEN', () => {
        const customFen = 'XXXXXXXX/XXXXXXXX/XXXXXXXX/XXXXXXXX/......../......../PPPPPPPP/RNBQKBNR';
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
        const customFen = 'XXXXXX.X/XXnXXX.X/XX.p1p2/XX...P.X/pp1PNB2/...X.X.P/PP5Q/K1R3R1';
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
