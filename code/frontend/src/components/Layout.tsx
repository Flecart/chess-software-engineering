import { useIsGuest } from '@/features/auth';
import { useTokenContext } from '@/lib/tokenContext';
import {
    EditOutlined,
    FormOutlined,
    PlayCircleOutlined,
    RobotOutlined,
    TrophyOutlined,
    UserOutlined,
} from '@ant-design/icons';
import { Link, Outlet } from '@tanstack/react-router';
import { Button, Flex, Layout as LibLayout, Menu, type MenuProps } from 'antd';
import ChessLogo from '/colored_knight.svg';

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
        <Link to="/game/" search={{ bot: false }}>
            Gioca
        </Link>,
        'online',
        <PlayCircleOutlined />,
    ),
    getItem(
        <Link to="/game/" search={{ bot: true }}>
            Pratica
        </Link>,
        'bot',
        <RobotOutlined />,
    ),
    getItem(<Link to="/leaderboard">Classifica</Link>, 'leaderboard', <TrophyOutlined />),
];

const menuItemsNotLogged: MenuProps['items'] = [
    getItem(<Link to="/register">Registrati</Link>, 'register', <FormOutlined />),
    getItem(<Link to="/login">Login</Link>, 'login', <EditOutlined />),
];

const menuItemsLogged: MenuProps['items'] = [getItem(<Link to="/profile/">Profilo</Link>, 'profile', <UserOutlined />)];

export const Layout = () => {
    const { token, unsetToken } = useTokenContext();
    const isGuest = useIsGuest(token);
    const showLoggedInfo = token !== null && !isGuest;

    const menuItems: MenuProps['items'] = [
        ...menuItemsClassic,
        { type: 'divider' },
        ...(showLoggedInfo ? menuItemsLogged : menuItemsNotLogged),
    ];

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
                    <Button onClick={unsetToken} ghost style={{ display: 'block', margin: '0 auto' }}>
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
