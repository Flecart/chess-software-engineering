import { signal } from '@preact/signals-react';

// my time
// remaining
export const myRemainingTime = signal<number>(0);
// start
export const myTimeStart = signal<string | null>(null);
// opponent time
// remaining
export const opponentRemainingTime = signal<number>(0);
// start
export const opponentTimeStart = signal<string | null>(null);
