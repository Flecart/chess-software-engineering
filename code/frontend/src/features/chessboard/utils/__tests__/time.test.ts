import { describe, expect, it } from 'vitest';
import { createExpireTime, displayTimer, parseTimeDelta, parseTimings } from '../time';

describe('parseTimeDelta', () => {
    it('should correctly parse a valid time delta', () => {
        const timeDelta = '01:30:15';
        const result = parseTimeDelta(timeDelta);
        expect(result).toEqual(5415);
    });

    it('should throw an error for an invalid time delta', () => {
        const timeDelta = '01:30';
        expect(() => parseTimeDelta(timeDelta)).toThrow('Invalid time delta');
    });

    it('should correctly parse a time delta with leading zeros', () => {
        const timeDelta = '01:05:09';
        const result = parseTimeDelta(timeDelta);
        expect(result).toEqual(3909);
    });

    it('should correctly parse a time delta with no leading zeros', () => {
        const timeDelta = '1:1:1';
        const result = parseTimeDelta(timeDelta);
        expect(result).toEqual(3661);
    });

    it('should correctly parse a time delta with only seconds', () => {
        const timeDelta = '00:00:30';
        const result = parseTimeDelta(timeDelta);
        expect(result).toEqual(30);
    });

    it('should correctly parse a time delta with only minutes', () => {
        const timeDelta = '00:30:00';
        const result = parseTimeDelta(timeDelta);
        expect(result).toEqual(1800);
    });

    it('should correctly parse a time delta with only hours', () => {
        const timeDelta = '01:00:00';
        const result = parseTimeDelta(timeDelta);
        expect(result).toEqual(3600);
    });
});

describe('createExpireTime', () => {
    it('should correctly calculate the expire time when time_start is provided', () => {
        const timeStart = '2023-11-26T11:41:49.563544';
        const timeLeft = '00:30:00';
        const result = createExpireTime(timeStart, timeLeft);
        const expected = new Date('2023-11-26T12:11:49.563544');
        expect(result).toEqual(expected);
    });

    it('should correctly calculate the expire time when time_start is null', () => {
        const timeStart = null;
        const timeLeft = '00:30:00';
        const result = createExpireTime(timeStart, timeLeft);
        const expected = new Date(new Date().getTime() + 1800 * 1000);
        expect(result.getTime()).toBeCloseTo(expected.getTime(), -2); // -2 for allowing 10ms difference
    });

    it('should throw an error for an invalid time_left', () => {
        const timeStart = '2023-11-26T11:41:49.563544';
        const timeLeft = '00:30';
        expect(() => createExpireTime(timeStart, timeLeft)).toThrow('Invalid time delta');
    });
});

describe('displayTimer', () => {
    it('should correctly format time when days, hours, minutes, and seconds are present', () => {
        const result = displayTimer(2, 13, 46, 40);
        expect(result).toEqual('02d : 13h : 46m : 40s');
    });

    it('should correctly format time when only hours, minutes, and seconds are present', () => {
        const result = displayTimer(0, 13, 46, 40);
        expect(result).toEqual('13h : 46m : 40s');
    });

    it('should correctly format time when only minutes and seconds are present', () => {
        const result = displayTimer(0, 0, 46, 40);
        expect(result).toEqual('46m : 40s');
    });

    it('should correctly format time when only seconds are present', () => {
        const result = displayTimer(0, 0, 0, 40);
        expect(result).toEqual('00m : 40s');
    });

    it('should correctly format time when all values are single digit', () => {
        const result = displayTimer(1, 1, 1, 1);
        expect(result).toEqual('01d : 01h : 01m : 01s');
    });

    it('should correctly format time when all values are zero', () => {
        const result = displayTimer(0, 0, 0, 0);
        expect(result).toEqual('00m : 00s');
    });
});

describe('parseTimings', () => {
    it('should correctly parse timings for white', () => {
        const timings = {
            time_left_white: '01:30:15',
            time_left_black: '02:15:30',
            time_start_white: '2023-11-26T11:41:49.563544',
            time_start_black: '2023-11-26T12:41:49.563544',
        };
        const result = parseTimings('white', timings);
        expect(result).toEqual({
            myTimeStart: '2023-11-26T11:41:49.563544',
            opponentTimeStart: '2023-11-26T12:41:49.563544',
            myTimeLeft: '01:30:15',
            opponentTimeLeft: '02:15:30',
        });
    });

    it('should correctly parse timings for black', () => {
        const timings = {
            time_left_white: '01:30:15',
            time_left_black: '02:15:30',
            time_start_white: '2023-11-26T11:41:49.563544',
            time_start_black: '2023-11-26T12:41:49.563544',
        };
        const result = parseTimings('black', timings);
        expect(result).toEqual({
            myTimeStart: '2023-11-26T12:41:49.563544',
            opponentTimeStart: '2023-11-26T11:41:49.563544',
            myTimeLeft: '02:15:30',
            opponentTimeLeft: '01:30:15',
        });
    });

    it('should correctly handle null timings', () => {
        const timings = {
            time_left_white: null,
            time_left_black: null,
            time_start_white: null,
            time_start_black: null,
        };
        const result = parseTimings('white', timings);
        expect(result).toEqual({
            myTimeStart: null,
            opponentTimeStart: null,
            myTimeLeft: '0:0:0',
            opponentTimeLeft: '0:0:0',
        });
    });

    it('should correctly handle partial null timings', () => {
        const timings = {
            time_left_white: '01:30:15',
            time_left_black: null,
            time_start_white: '2023-11-26T11:41:49.563544',
            time_start_black: null,
        };
        const result = parseTimings('white', timings);
        expect(result).toEqual({
            myTimeStart: '2023-11-26T11:41:49.563544',
            opponentTimeStart: null,
            myTimeLeft: '01:30:15',
            opponentTimeLeft: '0:0:0',
        });
    });
});
