// TODO: Consider integration with useBayesianFileUpload (~70% common logic) before rename
// TODO: Rename to useLoadReliabilityResult - current name doesn't clearly indicate purpose

import { useNavigate } from 'react-router-dom';
import { useAppState } from '../contexts/AppStateContext';

export const useReliabilityFileUpload = () => {
  const navigate = useNavigate();
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
          // Preserve the full uploaded JSON text for the Raw viewer
          (output as any).__rawText = fileContent;
        }
        setResults(output);
        setSimulationInput(data.input || null);
        setJobId('local');
        setJobStatus('COMPLETED');
        setError(null);
        navigate('/reliability-views/local');
        setPendingFile(null);
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