import { queryClient } from '@/lib/react-query';
import { router } from '@/routes';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { RouterProvider } from '@tanstack/react-router';
import { ConfigProvider as AntdConfigProvider, theme } from 'antd';
import itIT from 'antd/lib/locale/it_IT';

export const App = () => {
    return (
        <AntdConfigProvider
            // Customize theme
            theme={{
                algorithm: theme.defaultAlgorithm,
            }}
            locale={itIT}
        >
            <QueryClientProvider client={queryClient}>
                <RouterProvider router={router} />
                <ReactQueryDevtools buttonPosition="top-right" />
            </QueryClientProvider>
        </AntdConfigProvider>
    );
};
