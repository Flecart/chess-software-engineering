import { queryClient } from '@/lib/react-query';
import { TokenProvider } from '@/lib/tokenContext';
import { router } from '@/routes';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { RouterProvider } from '@tanstack/react-router';
import { ConfigProvider as AntdConfigProvider, theme } from 'antd';
import itIT from 'antd/lib/locale/it_IT';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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
                    <ToastContainer
                        position="bottom-right"
                        autoClose={5000}
                        hideProgressBar={true}
                        closeOnClick={true}
                        pauseOnHover={true}
                        draggable={true}
                        theme="colored"
                    />
                    <ReactQueryDevtools buttonPosition="top-right" />
                </QueryClientProvider>
            </AntdConfigProvider>
        </TokenProvider>
    );
};
