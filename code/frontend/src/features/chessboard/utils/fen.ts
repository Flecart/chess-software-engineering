import type { CustomSquareStyles, Piece, Square } from 'react-chessboard/dist/chessboard/types';
import { color } from '../types';
const fogChar = '?';

/**
 * Converts a non standard fen string to a standard fen string
 * the difference between the two is:
 * - the non standard fen string uses '.' to represent empty spaces
 * - the non standard fen string uses 'X' to represent fog spaces
 *
 * @param customFen the non standard fen string
 * @returns a standard fen string
 */
export function generateStandardFen(customFen: string): string {
    let fen = '';
    let emptySpaces = 0;

    for (let i = 0; i < customFen.length; i++) {
        const char = customFen.charAt(i);

        if (char === '.') {
            emptySpaces++;
        } else if (char === fogChar) {
            emptySpaces++;
        } else if (char >= '0' && char <= '9') {
            emptySpaces += parseInt(char);
        } else {
            if (emptySpaces > 0) {
                fen += emptySpaces;
                emptySpaces = 0;
            }
            fen += char;
        }
    }

    if (emptySpaces > 0) {
        fen += emptySpaces;
    }

    return fen;
}

/**
 * Converts a standard fen string to a non standard fen string
 * The new fen format uses numbers to represent empty spaces
 *
 * The old Fog fen uses plain dots
 * @param newFenFormat the standard fen string
 * @returns a non standard (old) fen string
 */
export function generateOldFogFen(newFenFormat: string): string {
    let fen = '';

    for (let i = 0; i < newFenFormat.length; i++) {
        const char = newFenFormat.charAt(i);
        if (char === ' ') break; // old format doesn't use the last part of the fen

        if (char >= '0' && char <= '9') {
            const value = parseInt(char);
            for (let j = 0; j < value; j++) {
                fen += '.';
            }
        } else {
            fen += char;
        }
    }
    return fen;
}

/**
 *
 * Generates an object that maps every fog tiles to a custom CSS style object
 *
 * @param customFen the non standard fen string
 */
export function generateFogObject(customFen: string): CustomSquareStyles {
    const fogObject: CustomSquareStyles = {};
    const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;

    // split the fen into an array
    // each element of the array is a row of the board,
    // reverse the array so the first element is the row number 1
    const rowsArray = customFen.split('/').reverse();

    rowsArray.forEach((row, i) => {
        for (let j = 0; j < row.length; j++) {
            const char = row.charAt(j);

            if (char === fogChar) {
                const number = i + 1;
                const letter = labels.at(j);
                const key = `${letter}${number}` as Square; // even if I define unexsisting square's key, it's fine because they will be ignored
                fogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' }; // TODO: create cooler custom fog
            }
        }
    });
    return fogObject;
}

/**
 * Returns what piece is occupying the given square
 * @param fen the fen string
 * @param square the square to check
 */

export function getPieceAtSquare(fen: string, square: Square): Piece | null {
    const rows = generateOldFogFen(fen).split('/').reverse();
    const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;

    const number = parseInt(square.charAt(1)) - 1;
    const letter = labels.indexOf(square.charAt(0));

    const row = rows[number] ?? '........';
    const char = row.charAt(letter);

    if (char === '.' || char === fogChar) return null;
    else if (char === char.toLowerCase()) return `b${char.toUpperCase()}` as Piece;
    else return `w${char}` as Piece;
}

/**
 * Return a boolean that tells if a Square is occupied by a piece of the given color, if the square is empty or fogged it returns false
 * @param fen the fen string
 * @param square the square to check
 * @param color the color of the piece
 * @returns a boolean that tells if a Square is occupied by a piece of the given color
 */
export function isSquareOccupiedByColor(fen: string, square: Square, color: color) {
    const rows = generateOldFogFen(fen).split('/').reverse();
    const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] as const;

    const number = parseInt(square.charAt(1)) - 1;
    const letter = labels.indexOf(square.charAt(0));

    const row = rows[number] ?? '........';
    const char = row.charAt(letter);

    if (char === '.' || char === fogChar) return false;
    if (color === 'white' && char === char.toUpperCase()) return true;
    if (color === 'black' && char === char.toLowerCase()) return true;
    return false;
}
