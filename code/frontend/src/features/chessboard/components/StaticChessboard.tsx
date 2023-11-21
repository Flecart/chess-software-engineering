import { Chessboard as ReactChessboard } from 'react-chessboard';
import { generateFogObject, generateOldFogFen, generateStandardFen } from '../utils/fen';

type Props = {
    customFEN: string;
    style?: React.CSSProperties;
};

export const StaticChessboard = (props: Props) => {
    return (
        <div
            style={{
                width: 'max(25vw, 250px)',
                ...props.style,
            }}
        >
            <ReactChessboard
                id="staticboard"
                position={generateStandardFen(props.customFEN)}
                customSquareStyles={generateFogObject(generateOldFogFen(props.customFEN))}
                arePiecesDraggable={false}
                areArrowsAllowed={false}
                arePremovesAllowed={false}
            />
        </div>
    );
};
