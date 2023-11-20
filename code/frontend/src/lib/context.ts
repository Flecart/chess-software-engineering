import React from 'react';

import type { jwt_token } from '@/types';

export const TokenContext = React.createContext<{
    token: jwt_token | null;
    setToken: (arg0: jwt_token | null) => void;
}>({
    token: null,
    setToken: () => {},
});
