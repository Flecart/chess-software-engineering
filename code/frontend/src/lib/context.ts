import React, { type Dispatch, type SetStateAction } from 'react';

import type { jwt_token } from '@/types';

export const TokenContext = React.createContext<{
    token: jwt_token | null;
    setToken: Dispatch<SetStateAction<string | null>>;
}>({
    token: null,
    setToken: () => {},
});
