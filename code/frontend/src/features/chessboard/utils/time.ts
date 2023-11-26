export function parseTimeDelta(timeDelta: string): number {
    const parts = timeDelta.split(/[:.]/);
    if (parts.length < 3) throw new Error('Invalid time delta');
    // TODO: a volte c'è anche millisecondi, non sempre, non lo stiamo gestendo, non
    // so se è importante, forse non si nota.

    const hours = parseInt(parts[0] as string, 10);
    const minutes = parseInt(parts[1] as string, 10);
    const seconds = parseInt(parts[2] as string, 10);

    const totalSeconds = hours * 60 * 60 + minutes * 60 + seconds;

    return totalSeconds;
}
