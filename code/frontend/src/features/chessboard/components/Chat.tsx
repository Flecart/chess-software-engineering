import { List, Typography } from 'antd';


type Props = Readonly<{
    messages: string[];
}>;

export const Chat = ({messages}: Props) => {
    const reversed_messages = [...messages].reverse();
    return (
        <List
            header={
                <Typography.Text strong style={{ fontSize: '1.5em' }}>
                    CHAT
                </Typography.Text>
            }
            bordered
            dataSource={reversed_messages}
            renderItem={(item) => (
                <List.Item
                    style={{
                        backgroundColor: '#e5e4e2',
                        border: '0.5px solid',
                        borderColor: 'ActiveBorder',
                        margin: '10px',
                        borderRadius: '7px',
                        boxShadow: '1px 1px 4px rgba(0, 0, 0, 0.2)',
                    }}
                >
                    <Typography.Text>{item}</Typography.Text>
                </List.Item>
            )}
            className="chatbox"
        />
    );
};
