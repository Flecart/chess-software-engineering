import { TokenProvider } from '@/lib/tokenContext';
import { router } from '@/routes';
import { RouterProvider } from '@tanstack/react-router';
import { ConfigProvider as AntdConfigProvider, theme } from 'antd';
import itIT from 'antd/lib/locale/it_IT';
import { queryClient } from '@/lib/react-query';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

export const App = () => {
    return (
        <TokenProvider>
            <AntdConfigProvider
                // Customize theme
                theme={{
                    algorithm: theme.defaultAlgorithm,
                }}
                locale={itIT}
            >
                <QueryClientProvider client={queryClient}>
                    <RouterProvider router={router} />
                    <ReactQueryDevtools />
                </QueryClientProvider>
            </AntdConfigProvider>
        </TokenProvider>
    );
};
