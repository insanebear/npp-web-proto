// FILE: src/shared/hooks/useFileUpload.ts

import { useAppState } from '../contexts/AppStateContext';

export const useFileUpload = () => {
  const { setPendingFile } = useAppState();

  const handleFileSelect = (file: File) => {
    setPendingFile(file);
  };

  return {
    handleFileSelect,
  };
};