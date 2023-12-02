import { Button } from 'antd';
import TwitterOutlined from '@ant-design/icons/TwitterOutlined';

//twitter share button
type Props = Readonly<{
    gameId: string;
}>;

export const TwitterShareButton = ({ gameId }: Props) => {
    const encodedGameId = encodeURIComponent(`Gioca con me usando questo id di unione alla partita: ${gameId}`);
    const encodedUrl = encodeURIComponent(`https://app.t1-check-mates.mooo.com/game`);
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodedGameId}&url=${encodedUrl}`;

    return (
        <>
            <Button type="primary" shape="round" icon={<TwitterOutlined />} href={twitterUrl} size="small">
                Tweet
            </Button>
        </>
    );
};
