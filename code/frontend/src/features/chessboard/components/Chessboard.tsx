import { Chessboard as ReactChessboard } from 'react-chessboard';

export const Chessboard = () => {
    return (
        <div
            style={{
                width: `70vw`,
                maxWidth: '70vh',
                margin: '3rem auto',
            }}
        >
            <ReactChessboard id="mainboard" />
        </div>
    );
};
