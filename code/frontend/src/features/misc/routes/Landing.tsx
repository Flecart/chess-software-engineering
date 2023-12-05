import { StaticChessboard } from '@/features/chessboard';
import { useNavigate } from '@tanstack/react-router';
import { Button, Flex, Typography } from 'antd';

export const Landing = () => {
    const navigate = useNavigate({ from: '/game' as const });

    return (
        <Flex align="center" justify="center" gap={'large'} wrap="wrap" style={{ marginTop: '50px' }}>
            <StaticChessboard customFEN="??????.?/??n???.?/??.p1p2/??...P.?/pp1PNB2/...?.?.P/PP5Q/K1R3R1" />
            <Flex gap="large" vertical style={{ maxWidth: '540px' }}>
                <Typography.Title>Federazione Italiana Scacchisti Eterodossi - Check Mates</Typography.Title>
                <Typography.Paragraph style={{ textAlign: 'justify' }}>
                    Dark chess è una variante degli scacchi con informazione incompleta, simile al Kriegspiel. È stato
                    inventato da Jens Bæk Nielsen e Torben Osted nel 1989. Un giocatore non vede l'intera scacchiera -
                    solo i propri pezzi e le caselle in cui può legalmente muoversi.
                </Typography.Paragraph>
            </Flex>
            <Flex justify="center" gap={100} wrap="wrap" style={{ width: '100%', marginTop: '120px' }}>
                <Button
                    type="primary"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game/', search: { bot: true } });
                    }}
                >
                    Gioca contro il computer
                </Button>
                <Button
                    type="default"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/game/', search: { bot: false } });
                    }}
                >
                    Gioca Online
                </Button>
            </Flex>
            <Flex justify="center" gap={100} wrap="wrap" style={{ width: '100%', marginTop: '2rem' }}>
                <Button
                    type="primary"
                    size="large"
                    onClick={() => {
                        navigate({ to: '/darkboard' });
                    }}
                >
                    Guarda Darkboard - OpenSpiel
                </Button>
            </Flex>
        </Flex>
    );
};
