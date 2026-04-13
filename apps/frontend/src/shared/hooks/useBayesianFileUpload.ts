// TODO: Consider integration with useReliabilityFileUpload (~70% common logic) before rename
// TODO: Rename to useLoadBayesianInput - current name doesn't clearly indicate purpose

import { useAppState } from '../contexts/AppStateContext';

type SettingsSnapshot = {
  nChains: number;
  nIter: number;
  nBurnin: number;
  nThin: number;
};

export const useBayesianFileUpload = (onSettingsLoad?: (values: SettingsSnapshot) => void) => {
  const {
    setResults,
    setSimulationInput,
    setInputValues,
    setError,
    setPendingFile,
    initializeInputState,
  } = useAppState();

  const handleBayesianUpload = (fileContent: string) => {
    try {
      const data = JSON.parse(fileContent);
      if (typeof data === 'object' && data !== null && data.input && data.output) {
        setResults(data.output);
        setSimulationInput(data.input);
        const { settings } = data.input;
        if (settings && onSettingsLoad) {
          onSettingsLoad({
            nChains: Number(settings.nChains),
            nIter: Number(settings.nIter),
            nBurnin: Number(settings.nBurnin),
            nThin: Number(settings.nThin),
          });
        }
        setInputValues(initializeInputState(data.input));
        setError(null);
        alert("Inputs and settings have been loaded from the file. Results are available on the Analysis Result.");
        setPendingFile(null);
      } else {
        throw new Error("Invalid file. JSON must contain 'input' and 'output' keys.");
      }
    } catch (err: any) {
      setError(err.message || 'Failed to parse the uploaded file.');
    }
  };

  return {
    handleBayesianUpload,
  };
};
