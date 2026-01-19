import { useState, useEffect, type Dispatch, type SetStateAction } from 'react';

export type AppSettings = {
  nChains: number;
  nIter: number;
  nBurnin: number;
  nThin: number;
  workingDir: string;
  setnChains: Dispatch<SetStateAction<number>>;
  setnIter: Dispatch<SetStateAction<number>>;
  setnBurnin: Dispatch<SetStateAction<number>>;
  setnThin: Dispatch<SetStateAction<number>>;
  setworkingDir: Dispatch<SetStateAction<string>>;
};

const STORAGE_KEY = 'appSettings';

const defaultSettings = {
  nChains: 1,
  nIter: 20000,
  nBurnin: 500,
  nThin: 1,
  workingDir: '/app/results',
};

const loadSettings = () => {
  try {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      return {
        nChains: parsed.nChains ?? defaultSettings.nChains,
        nIter: parsed.nIter ?? defaultSettings.nIter,
        nBurnin: parsed.nBurnin ?? defaultSettings.nBurnin,
        nThin: parsed.nThin ?? defaultSettings.nThin,
        workingDir: parsed.workingDir ?? defaultSettings.workingDir,
      };
    }
  } catch (error) {
    console.error('Failed to load settings from sessionStorage:', error);
  }
  return defaultSettings;
};

const saveSettings = (settings: typeof defaultSettings) => {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch (error) {
    console.error('Failed to save settings to sessionStorage:', error);
  }
};

export const useAppSettings = (): AppSettings => {
  const [nChains, setnChainsState] = useState(() => loadSettings().nChains);
  const [nIter, setnIterState] = useState(() => loadSettings().nIter);
  const [nBurnin, setnBurninState] = useState(() => loadSettings().nBurnin);
  const [nThin, setnThinState] = useState(() => loadSettings().nThin);
  const [workingDir, setworkingDirState] = useState(() => loadSettings().workingDir);


  useEffect(() => {
    saveSettings({ nChains, nIter, nBurnin, nThin, workingDir });
  }, [nChains, nIter, nBurnin, nThin, workingDir]);

  const setnChains: Dispatch<SetStateAction<number>> = (value) => {
    setnChainsState(value);
  };

  const setnIter: Dispatch<SetStateAction<number>> = (value) => {
    setnIterState(value);
  };

  const setnBurnin: Dispatch<SetStateAction<number>> = (value) => {
    setnBurninState(value);
  };

  const setnThin: Dispatch<SetStateAction<number>> = (value) => {
    setnThinState(value);
  };

  const setworkingDir: Dispatch<SetStateAction<string>> = (value) => {
    setworkingDirState(value);
  };

  return {
    nChains, nIter, nBurnin, nThin, workingDir,
    setnChains, setnIter, setnBurnin, setnThin, setworkingDir
  };
};
