import { useState } from 'react';

// This hook receives two parameters:
// storageKey: This is the name of our storage that gets used when we retrieve/save our persistent data.
// fallbackState: This is our default value, but only if the store doesn't exist, otherwise it gets overwritten by the store.
export default <T>(storageKey: string, fallbackState: T): [T, (arg0: T) => void] => {
    const [state, setState] = useState<T>(getFromLocalStorage(storageKey) ?? fallbackState);

    const setPersistState = (newState: T): void => {
        localStorage.setItem(storageKey, JSON.stringify(newState));
        setState(newState);
    };

    return [state, setPersistState];
};

function getFromLocalStorage<T>(key: string): T | null {
    try {
        const storageInBrowser = localStorage.getItem(key);
        if (storageInBrowser !== null) {
            return JSON.parse(storageInBrowser) as T;
        }
    } catch (e) {
        console.error(e);
    }
    return null;
}
