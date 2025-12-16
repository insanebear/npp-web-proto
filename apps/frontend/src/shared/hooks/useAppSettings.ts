import { useState, type Dispatch, type SetStateAction } from 'react';

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

export const useAppSettings = (): AppSettings => {
  const [nChains, setnChains] = useState(4);
  const [nIter, setnIter] = useState(10000);
  const [nBurnin, setnBurnin] = useState(2000);
  const [nThin, setnThin] = useState(1);
  const [workingDir, setworkingDir] = useState('/app/results');

  return {
    nChains, nIter, nBurnin, nThin, workingDir,
    setnChains, setnIter, setnBurnin, setnThin, setworkingDir
  };
};
