import { Layout as LibLayout, Menu, Flex, type MenuProps, Button } from 'antd';
import { Link, Outlet } from '@tanstack/react-router';
import {
    PlayCircleOutlined,
    RobotOutlined,
    TrophyOutlined,
    FormOutlined,
    EditOutlined,
    UserOutlined,
} from '@ant-design/icons';
import ChessLogo from '/colored_knight.svg';
import { useTokenContext } from '@/lib/tokenContext';
import { useMemo } from 'react';
import { jwtDecode } from 'jwt-decode';

const { Sider, Content } = LibLayout;
type MenuItem = Required<MenuProps>['items'][number];

function getItem(
    label: React.ReactNode,
    key: React.Key,
    icon?: React.ReactNode,
    children?: MenuItem[],
    type?: 'group',
): MenuItem {
    return {
        key,
        icon,
        children,
        label,
        type,
    };
}

const menuItemsClassic: MenuProps['items'] = [
    getItem(
        <Link to="/game" search={{ bot: true }}>
            Gioca
        </Link>,
        'online',
        <PlayCircleOutlined />,
    ),
    getItem(<Link to="/404">Pratica</Link>, 'bot', <RobotOutlined />),
    getItem(<Link to="/leaderboard">Classifica</Link>, 'leaderboard', <TrophyOutlined />),
];

const menuItemsNotLogged: MenuProps['items'] = [
    getItem(<Link to="/register">Registrati</Link>, 'register', <FormOutlined />),
    getItem(<Link to="/login">Login</Link>, 'login', <EditOutlined />),
];

export const Layout = () => {
    const { token, setToken } = useTokenContext();

    const username = useMemo<string>(() => {
        const defValue = 'magnus';
        if (!token) return defValue;
        const decodedToken = jwtDecode(token);
        if ('sub' in decodedToken && (decodedToken.sub as string).startsWith('guest')) {
            return defValue;
        }
        return decodedToken.sub as string;
    }, [token]);

    const menuItemsLogged: MenuProps['items'] = [
        getItem(
            <Link to="/profile/$username" params={{ username }}>
                Profilo
            </Link>,
            'profile',
            <UserOutlined />,
        ),
    ];
    const isBot = useMemo(() => {
        if (!token) return false;
        const decodedToken = jwtDecode(token);
        console.log(decodedToken);
        // check if the decoded token has the username starting with guest
        if ('sub' in decodedToken && (decodedToken.sub as string).startsWith('guest')) {
            return true;
        }
        return false;
    }, [token]);

    const showLoggedInfo = useMemo(() => {
        return token !== null && !isBot;
    }, [token, isBot]);

    const menuItems: MenuProps['items'] = [
        ...menuItemsClassic,
        { type: 'divider' },
        ...(showLoggedInfo ? menuItemsLogged : menuItemsNotLogged),
    ];

    const unsetToken = () => {
        setToken(null);
    };

    return (
        <LibLayout style={{ height: '100vh', display: 'flex', gap: '1rem' }}>
            <Sider breakpoint="lg" collapsible style={{ overflowY: 'hidden' }}>
                <div style={{ padding: '2rem 1rem' }}>
                    <Link to="/">
                        <img src={ChessLogo} alt="Check Mates Logo" width={50} />
                    </Link>
                </div>
                <Flex vertical justify="space-between" style={{ height: '80%' }}>
                    <Menu theme="dark" mode="inline" items={menuItems} />
                </Flex>

                {showLoggedInfo && (
                    <Button onClick={unsetToken} ghost style={{ float: 'right', marginRight: '1rem' }}>
                        Logout
                    </Button>
                )}
            </Sider>
            <LibLayout style={{ flex: 1, overflow: 'auto' }}>
                <Content>
                    <Outlet />
                </Content>
            </LibLayout>
        </LibLayout>
    );
};
