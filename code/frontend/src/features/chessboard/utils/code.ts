// This is a function used to create the game codes, only too be more complex
// from the users eyes!

// non big per parte crittografica, ma deve solo sembrare all'utente qualcosa di complesso,
// in modo che faccia un po' di fatica a prendere altri giochi!
const bigPrime = 3412328917; // possiamo supportare fino 15 tipo con js interi 10k partite

export function createCode(gameId: string) {
    return (parseInt(gameId) * bigPrime).toString(16);
}

export function parseCode(code: string) {
    const intValue = parseInt(code, 16);
    if (intValue % bigPrime !== 0) {
        throw new Error('Invalid code');
    }
    return (intValue / bigPrime).toString();
}
