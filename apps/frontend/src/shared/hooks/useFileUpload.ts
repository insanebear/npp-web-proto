// FILE: src/shared/hooks/useFileUpload.ts

// TODO: Rename to useFileSelect - this hook only handles file selection, not upload
// Current name is misleading as it doesn't actually upload files

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