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
        } else {
            if (emptySpaces > 0) {
                fen += emptySpaces;
                emptySpaces = 0;
            }
            fen += char;
        }

        if (i === customFen.length - 1 && emptySpaces > 0) {
            fen += emptySpaces;
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
export function generateFogObject(customFen: string): {
    [key: string]: React.CSSProperties;
} {
    const fogObject: { [key: string]: React.CSSProperties } = {};
    const labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

    for (let i = 0; i < customFen.length; i++) {
        const char = customFen.charAt(i);

        if (char === 'X') {
            const row = 8 - Math.floor(i / 9);
            const col = labels.at(i % 9);
            const key = `${col}${row}`;
            fogObject[key] = { backgroundColor: 'rgba(21, 21, 21, 0.95)' }; // TODO: create cooler custom fog
        }
    }

    return fogObject;
}
