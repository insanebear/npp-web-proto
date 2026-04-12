import { createContext, useContext, useState, type ReactNode, type Dispatch, type SetStateAction } from 'react';

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

const defaultSettings = {
  nChains: 1,
  nIter: 20000,
  nBurnin: 500,
  nThin: 1,
  workingDir: '/app/results',
};

const AppSettingsContext = createContext<AppSettings | null>(null);

export const AppSettingsProvider = ({ children }: { children: ReactNode }) => {
  const [nChains, setnChains] = useState(defaultSettings.nChains);
  const [nIter, setnIter] = useState(defaultSettings.nIter);
  const [nBurnin, setnBurnin] = useState(defaultSettings.nBurnin);
  const [nThin, setnThin] = useState(defaultSettings.nThin);
  const [workingDir, setworkingDir] = useState(defaultSettings.workingDir);

  return (
    <AppSettingsContext.Provider value={{ nChains, nIter, nBurnin, nThin, workingDir, setnChains, setnIter, setnBurnin, setnThin, setworkingDir }}>
      {children}
    </AppSettingsContext.Provider>
  );
};

export const useAppSettings = (): AppSettings => {
  const ctx = useContext(AppSettingsContext);
  if (!ctx) throw new Error('useAppSettings must be used within AppSettingsProvider');
  return ctx;
};
