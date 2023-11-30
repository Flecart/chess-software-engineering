import { color } from '@/features/chessboard';

export type jwt_token = string;

export type GameRouteSearch = {
    boardOrientation: color;
};

export type PregameRouteSearch = {
    bot: boolean;
};

export type ErrorResponseData = {
    message: string;
};

export type MutationMeta = {
    onSuccessMessage?: string;
};
