import { describe, expect, it } from 'vitest';
import { generateFogObject, generateStandardFen } from '../fen';

describe('generateStandardFen', () => {
    it('should generate a standard FEN string from a already standard FEN string', () => {
        const customFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const expectedFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const result = generateStandardFen(customFen);
        expect(result).toEqual(expectedFen);
    });

    it('should handle "X" and the "." characters in the custom FEN string', () => {
        const customFen = 'XXXX.XXX/XXXXXXXX/......../......../......../......../PPPPPPPP/RNBQKBNR';
        const expectedFen = '8/8/8/8/8/8/PPPPPPPP/RNBQKBNR';
        const result = generateStandardFen(customFen);
        expect(result).toEqual(expectedFen);
    });

    it('should handle spaces as numbers in the custom FEN string', () => {
        const customFen = 'rnbqkbnr/XXXXXXXX/8/8/8/3P4/PPP1PPPP/RNBQKBNR';
        const expectedFen = 'rnbqkbnr/8/8/8/8/3P4/PPP1PPPP/RNBQKBNR';
        const result = generateStandardFen(customFen);
        expect(result).toEqual(expectedFen);
    });

    it('should handle a string with the last row empty in the custom FEN string', () => {
        const customFen = 'XXXX.XXX/XXXXXXXX/......../......../......../PPPPPPPP/RNBQKBNR/........';
        const expectedFen = '8/8/8/8/8/PPPPPPPP/RNBQKBNR/8';
        const result = generateStandardFen(customFen);
        expect(result).toEqual(expectedFen);
    });
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
});
