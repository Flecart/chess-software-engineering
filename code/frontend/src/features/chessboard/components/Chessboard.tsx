import { Chessboard as ReactChessboard } from 'react-chessboard';
import { generateFogObject, generateStandardFen } from '../utils/fen';

const customFEN = 'XXXXXXXX/XXXXXXXX/XXXXXXXX/XXX...XX/4P3/8/PPPP1PPP/RNBQKBNR';

export const Chessboard = () => {
    return (
        <div
            style={{
                width: `70vw`,
                maxWidth: '70vh',
                margin: '3rem auto',
            }}
        >
            <ReactChessboard
                id="mainboard"
                position={generateStandardFen(customFEN)}
                customSquareStyles={generateFogObject(customFEN)}
            />
        </div>
    );
};
