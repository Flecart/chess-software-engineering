export type color = 'white' | 'black';

type GameState = {
    ended: boolean;
    possible_moves: null | string[];
    view: string;
    move_made: null | string;
    turn: color;

    // TODO: refactor next sprint
    time_left_white: string | null;
    time_left_black: string | null;
    time_start_white: string | null;
    time_start_black: string | null;
};

type WaitingState = {
    waiting: true;
};

export type wsMessage = GameState | WaitingState | null;

export type GameOptions = {
    variant: 'dark_chess' | 'kriegspiel';
    time: number;
    color: color;
};

export type CreateGameParams = {
    against_bot: boolean;
    type: 'dark_chess' | 'kriegspiel';
    time: number;
};
