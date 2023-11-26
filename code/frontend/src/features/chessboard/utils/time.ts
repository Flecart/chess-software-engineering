function parseTimeDelta(timeDelta: string): number {
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

export const createExpireTime = (time_start: string | null, time_left: string) => {
    const timeStart = time_start ? new Date(time_start) : new Date();
    const timeLeft = parseTimeDelta(time_left);

    const resultingDate = new Date(timeStart.getTime() + timeLeft * 1000);

    return resultingDate;
};

export const displayTimer = (days: number, hours: number, minutes: number, seconds: number) => {
    const daysStr = days > 0 ? `${days.toString().padStart(2, '0')}d : ` : '';
    const hoursStr = hours > 0 ? `${hours.toString().padStart(2, '0')}h : ` : '';
    const minutesStr = minutes > 0 ? `${minutes.toString().padStart(2, '0')}m : ` : '';
    const secondsStr = seconds.toString().padStart(2, '0');

    return `${daysStr}${hoursStr}${minutesStr}${secondsStr}s`;
};
