import { useAppState } from '../contexts/AppStateContext';

export const useReliabilityFileUpload = (onLoaded?: () => void) => {
  const {
    setResults,
    setSimulationInput,
    setJobId,
    setJobStatus,
    setError,
    setPendingFile,
  } = useAppState();

  const handleReliabilityUpload = (fileContent: string) => {
    try {
      const data = JSON.parse(fileContent);
      if (typeof data === 'object' && data !== null && 'output' in data) {
        const output = (data as any).output;
        if (output && typeof output === 'object') {
          (output as any).__rawText = fileContent;
        }
        setResults(output);
        setSimulationInput(data.input || null);
        setJobId('local');
        setJobStatus('COMPLETED');
        setError(null);
        setPendingFile(null);
        onLoaded?.();
      } else {
        throw new Error("Invalid file. JSON must contain an 'output' key.");
      }
    } catch (err: any) {
      setError(err.message || 'Failed to parse the uploaded file.');
    }
  };

  return {
    handleReliabilityUpload,
  };
};