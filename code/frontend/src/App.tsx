import { router } from '@/routes';
import { RouterProvider } from '@tanstack/react-router';
import { ConfigProvider as AntdConfigProvider, theme } from 'antd';
import itIT from 'antd/lib/locale/it_IT';
import { TokenContext } from '@/lib/context';
import type { jwt_token } from '@/types';
import usePersistState from './features/hooks/usePersistState';

export const App = () => {
    const [token, setToken] = usePersistState<null | jwt_token>('jwt_token', null);
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
