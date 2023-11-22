import { describe, expect, it } from 'vitest';
import { createCode, parseCode } from '../code';

describe('parseCode', () => {
    it('should return the parsed code when the input is a valid hexadecimal code', () => {
        const code = '196c803aa';
        const expected = '2';
        const result = parseCode(code);
        expect(result).toEqual(expected);
    });

    it('should throw an error when the input is not a valid hexadecimal code', () => {
        const code = 'XYZ';
        expect(() => {
            parseCode(code);
        }).toThrow('Invalid code');
    });
});

describe('keep the translation consistent', () => {
    it("should keep the original code equal when it's obfuscated and parsed", () => {
        const code = '2';
        const result = parseCode(createCode(code));
        expect(result).toEqual(code);
    });

    it("should keep the obfuscated code equal when it's parsed and then obfuscated again", () => {
        const code = '7f1e81252';
        const result = createCode(parseCode(code));
        expect(result).toEqual(code);
    });
});
