import { useAppState } from '../contexts/AppStateContext';

export const useFileSelect = () => {
  const { setPendingFile } = useAppState();

  const handleFileSelect = (file: File) => {
    setPendingFile(file);
  };

  return {
    handleFileSelect,
  };
};