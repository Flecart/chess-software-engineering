type GameState = {
    ended: boolean;
    possible_moves: null | string[];
    view: string;
    move_made: null | string;
    turn: 'white' | 'black';

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
