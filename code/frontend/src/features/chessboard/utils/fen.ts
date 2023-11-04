import type { CustomSquareStyles, Square } from 'react-chessboard/dist/chessboard/types';
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
        } else if (char === 'X') {
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

            if (char === 'X') {
                const number = i + 1;
                const letter = labels.at(j);
                const key = `${letter}${number}` as Square; // even if I define unexsisting square's key, it's fine because they will be ignored
                fogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' }; // TODO: create cooler custom fog
            }
        }
    });
    return fogObject;
}
