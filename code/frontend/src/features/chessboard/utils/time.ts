import { color } from '../types';

/**
 * Parses a time delta string and returns the total number of seconds.
 * @param timeDelta - The time delta string in the format "HH:MM:SS".
 * @returns The total number of seconds.
 * @throws {Error} If the time delta string is invalid.
 */
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

/**
 * Creates an expire time based on the start time and the time left.
 * If the start time is null, the current time is used.
 * @param time_start - The start time in string format or null.
 * @param time_left - The time left in string format.
 * @returns The resulting expire time as a Date object.
 */
export function createExpireTime(time_start: string | null, time_left: string) {
    const timeStart = time_start ? new Date(time_start) : new Date();
    const timeLeft = parseTimeDelta(time_left);

    const resultingDate = new Date(timeStart.getTime() + timeLeft * 1000);

    return resultingDate;
}

/**
 * Formats the given time values into a displayable timer string.
 * @param days - The number of days.
 * @param hours - The number of hours.
 * @param minutes - The number of minutes.
 * @param seconds - The number of seconds.
 * @returns The formatted timer string.
 */
export function displayTimer(days: number, hours: number, minutes: number, seconds: number) {
    const daysStr = days > 0 ? `${days.toString().padStart(2, '0')}d : ` : '';
    const hoursStr = hours > 0 ? `${hours.toString().padStart(2, '0')}h : ` : '';
    const minutesStr = `${minutes.toString().padStart(2, '0')}m : `;
    const secondsStr = seconds.toString().padStart(2, '0');

    return `${daysStr}${hoursStr}${minutesStr}${secondsStr}s`;
}

/**
 * Parses the timings object and returns the time information for the specified player.
 * @param me - The color of the player ('white' or 'black').
 * @param timings - The timings object containing the time information.
 * @returns An object containing the start time and remaining time for the player and the opponent.
 */
export function parseTimings(
    me: color,
    timings: {
        time_left_white: string | null;
        time_left_black: string | null;
        time_start_white: string | null;
        time_start_black: string | null;
    },
) {
    const timeLeftWhite = timings.time_left_white ?? '0:0:0';
    const timeLeftBlack = timings.time_left_black ?? '0:0:0';

    const myTimeLeft = me === 'white' ? timeLeftWhite : timeLeftBlack;
    const opponentTimeLeft = me === 'black' ? timeLeftWhite : timeLeftBlack;

    const myTimeStart = me === 'white' ? timings.time_start_white : timings.time_start_black;
    const opponentTimeStart = me === 'black' ? timings.time_start_white : timings.time_start_black;
    return { myTimeStart, opponentTimeStart, myTimeLeft, opponentTimeLeft };
}
