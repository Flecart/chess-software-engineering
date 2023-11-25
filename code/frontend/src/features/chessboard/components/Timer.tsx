import React, { useState, useEffect, useCallback } from 'react';
import { ClockCircleOutlined } from '@ant-design/icons';

interface TimerProps {
    start?: number;
    stop?: boolean;
    onZero?: () => void;
}

const Timer: React.FC<TimerProps> = ({ start = 0, stop = false, onZero }) => {
    /*la prima mossa lo vedi perchè start non è settato semplicemente quindi ti dovrebbe arrivare un valore nullo*/
    // c'è i parametri che ti arrivano
    // sono entrambi a None
    // perchè i timer non sono partiti
    // capito?
    // mi puoi andare sul ws
    const [seconds, setSeconds] = useState<number>(start);

    const displayTimer = useCallback(() => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor(seconds / 60);
        const secondsLeft = seconds % 60;

        if (seconds <= 0) {
            return '0m:0s';
        }

        let out = '';
        if (hours > 0) {
            out += `${hours}h:`;
        }
        return `${out}${minutes}m:${secondsLeft < 10 ? '0' : ''}${secondsLeft}s`;
    }, [seconds]);

    useEffect(() => {
        setSeconds(start);
    }, [start]);

    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (!stop) {
            interval = setInterval(() => {
                setSeconds((seconds) => {
                    if (seconds <= 0) {
                        if (onZero) {
                            onZero();
                        }
                        clearInterval(interval);
                    }
                    return seconds - 1;
                });
            }, 1000);
        }

        return () => {
            if (interval) {
                clearInterval(interval);
            }
        };
    }, [stop, onZero]);

    return (
        <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                fontSize: '2em',
                fontWeight: 'bold',
                color: '#333',
                background: '#f5f5f5',
            }}
        >
            <ClockCircleOutlined />
            <pre> </pre>
            {displayTimer()}
        </div>
    );
};

export default Timer;
