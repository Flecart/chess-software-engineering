import { Chessboard } from './features/chessboard';
import { Button } from 'antd';

export const App = () => {
    return (
        <>
            <Chessboard gameId="" />
            <Button>Start Game</Button>
        </>
    );
};
