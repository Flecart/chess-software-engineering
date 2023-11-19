import { useState } from 'react';
import { router } from '@/routes';
import { RouterProvider } from '@tanstack/react-router';
import { ConfigProvider as AntdConfigProvider, theme } from 'antd';
import itIT from 'antd/lib/locale/it_IT';
import { TokenContext } from './lib/context';
import type { jwt_token } from './features/auth/api/auth';

export const App = () => {
    const [token, setToken] = useState<null | jwt_token>(null);
    return (
        <TokenContext.Provider value={{ token, setToken }}>
            <AntdConfigProvider
                // Customize theme
                theme={{
                    algorithm: theme.defaultAlgorithm,
                }}
                locale={itIT}
            >
                <RouterProvider router={router} />
            </AntdConfigProvider>
        </TokenContext.Provider>
    );
};
