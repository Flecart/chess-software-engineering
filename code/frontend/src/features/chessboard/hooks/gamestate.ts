import { signal } from '@preact/signals';

// turn
export const isMyTurn = signal<boolean>(false);

// game ended
export const gameEnded = signal<boolean>(false);

// fen
export const fen = signal<string>('');
