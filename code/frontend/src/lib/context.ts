import React, { type Dispatch, type SetStateAction } from 'react';

export const TokenContext = React.createContext<{
    token: string | null;
    setToken: Dispatch<SetStateAction<string | null>>;
}>({
    token: null,
    setToken: () => {},
});
