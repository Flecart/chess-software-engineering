import { router } from '@/routes';
import { RouterProvider } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';
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
            <RouterProvider router={router} />
            <TanStackRouterDevtools router={router} position="bottom-right" />
        </AntdConfigProvider>
    );
};
