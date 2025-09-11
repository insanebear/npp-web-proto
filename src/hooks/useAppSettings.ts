// FILE: src/hooks/useAppSettings.ts

import { useState, Dispatch, SetStateAction } from 'react';

// FIXED: Changed from 'interface' to 'type' for better module compatibility
export type AppSettings = {
  nChains: number;
  nIter: number;
  nBurnin: number;
  nThin: number;
  computeDIC: boolean;
  workingDir: string;
  setnChains: Dispatch<SetStateAction<number>>;
  setnIter: Dispatch<SetStateAction<number>>;
  setnBurnin: Dispatch<SetStateAction<number>>;
  setnThin: Dispatch<SetStateAction<number>>;
  setcomputeDIC: Dispatch<SetStateAction<boolean>>;
  setworkingDir: Dispatch<SetStateAction<string>>;
};

export const useAppSettings = (): AppSettings => {
  const [nChains, setnChains] = useState(4);
  const [nIter, setnIter] = useState(10000);
  const [nBurnin, setnBurnin] = useState(2000);
  const [nThin, setnThin] = useState(1);
  const [computeDIC, setcomputeDIC] = useState(true);
  const [workingDir, setworkingDir] = useState('/app/results');

  return {
    nChains, nIter, nBurnin, computeDIC, nThin, workingDir,
    setnChains, setnIter, setnBurnin, setcomputeDIC, setnThin, setworkingDir
  };
};