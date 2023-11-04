import { Layout as LibLayout, Menu } from 'antd';
import { Link, Outlet } from '@tanstack/react-router';
import { PlayCircleOutlined, RobotOutlined, TrophyOutlined } from '@ant-design/icons';
import ChessLogo from '/colored_knight.svg';
import type { MenuProps } from 'antd';

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

const menuItems: MenuProps['items'] = [
    getItem(<Link to="/game">Gioca</Link>, 'online', <PlayCircleOutlined />),
    getItem(<Link to="/404">Pratica</Link>, 'bot', <RobotOutlined />),
    getItem(<Link to="/404">Classifica</Link>, 'leaderboard', <TrophyOutlined />),
];

export const Layout = () => {
    return (
        <LibLayout style={{ minHeight: '100vh' }}>
            <Sider breakpoint="lg" collapsible>
                <div style={{ padding: '2rem 1rem' }}>
                    <Link to="/">
                        <img src={ChessLogo} alt="Check Mates Logo" width={50} />
                    </Link>
                </div>
                <Menu theme="dark" mode="inline" items={menuItems} />
            </Sider>
            <LibLayout style={{ marginLeft: 'min(1vw,20px)' }}>
                <Content>
                    <Outlet />
                </Content>
            </LibLayout>
        </LibLayout>
    );
};
