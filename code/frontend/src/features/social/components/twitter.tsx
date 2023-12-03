import { frontendUrl } from '@/config';
import TwitterOutlined from '@ant-design/icons/TwitterOutlined';
import { Button } from 'antd';

//twitter share button
type Props = Readonly<{
    gameId: string;
}>;

export const TwitterShareButton = ({ gameId }: Props) => {
    const encodedGameId = encodeURIComponent(
        `Gioca con me sul sito di Check Mates! Il link per entrare nella partita è:`,
    );
    const encodedUrl = encodeURIComponent(`${frontendUrl}/game/?bot=false&sharedGameId=${gameId}`);
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodedGameId}&url=${encodedUrl}&hashtags=CheckMates,Scacchi,VariantiDiScacchi`;

    return (
        <Button type="primary" shape="round" icon={<TwitterOutlined />} href={twitterUrl} target="_blank" size="small">
            Tweet
        </Button>
    );
};
