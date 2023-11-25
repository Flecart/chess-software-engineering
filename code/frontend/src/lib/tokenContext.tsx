import { createContext, useContext, useMemo, type ReactNode } from 'react';

import usePersistState from '@/hooks/usePersistState';
import type { jwt_token } from '@/types';

type TokenContextProps = {
    token: jwt_token | null;
    setToken: (prevToken: jwt_token | null) => void;
    unsetToken: () => void;
};

export const TokenContext = createContext<TokenContextProps>({
    token: null,
    setToken: () => null,
    unsetToken: () => null,
});

// eslint-disable-next-line react-refresh/only-export-components
export const useTokenContext = () => {
    return useContext(TokenContext);
};

export const TokenProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = usePersistState<jwt_token | null>('jwt_token', null);

    const value = useMemo(
        () => ({
            token,
            setToken,
            unsetToken: () => {
                setToken(null);
            },
        }),
        [token, setToken],
    );

    return <TokenContext.Provider value={value}>{children}</TokenContext.Provider>;
};
