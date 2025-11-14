import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import { TABS } from '../constants/tabs';
import { getCodeKey } from '../constants/labelToCode';

// ===========================================
// HELPER FUNCTIONS
// ===========================================

/**
 * Initialize or reset all input values to their default state
 * @param initialData - Optional data to pre-populate inputs
 * @returns Initial state object for input values
 */
const initializeInputState = (initialData?: any) => {
  const initialState: Record<string, string> = {};
  TABS.forEach(tab => {
    tab.children.forEach(child => {
      const key = `${tab.label}/${child.label}`;
      const uploadedSection = initialData?.[tab.label] || {};
      const uploadedValueByLabel = uploadedSection?.[child.label];
      const codeKey = getCodeKey(tab.label, child.label) || child.label;
      const uploadedValueByCode = uploadedSection?.[codeKey];

      // Special handling for the new FP input
      if (tab.label === 'FP') {
        initialState[key] = uploadedValueByLabel ?? uploadedValueByCode ?? '56'; // Default FP to 56
      } else {
        // Use the uploaded value, or default to 'Medium' for dropdowns
        initialState[key] = (uploadedValueByLabel ?? uploadedValueByCode) || child.values[1];
      }
    });
  });
  return initialState;
};

// ===========================================
// CONTEXT TYPE DEFINITION
// ===========================================

interface AppStateContextType {
  // Simulation-related state
  jobId: string | null;
  jobStatus: string | null;
  results: any | null;
  error: string | null;
  simulationInput: object | null;

  // File-related state
  pendingFile: File | null;

  // Input values state
  inputValues: { [key: string]: string };

  // State setters
  setJobId: (id: string | null) => void;
  setJobStatus: (status: string | null) => void;
  setResults: (results: any | null) => void;
  setError: (error: string | null) => void;
  setSimulationInput: (input: object | null) => void;
  setPendingFile: (file: File | null) => void;
  setInputValues: (values: { [key: string]: string } | ((prev: { [key: string]: string }) => { [key: string]: string })) => void;

  // Helper function
  initializeInputState: (initialData?: any) => { [key: string]: string };
}

// ===========================================
// CONTEXT CREATION
// ===========================================

const AppStateContext = createContext<AppStateContextType | undefined>(undefined);

// ===========================================
// PROVIDER COMPONENT
// ===========================================

interface AppStateProviderProps {
  children: ReactNode;
}

export const AppStateProvider = ({ children }: AppStateProviderProps) => {
  // Simulation-related state
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [results, setResults] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [simulationInput, setSimulationInput] = useState<object | null>(null);

  // File-related state
  const [pendingFile, setPendingFile] = useState<File | null>(null);

  // Input values state (unified state for all form inputs)
  const [inputValues, setInputValues] = useState(() => initializeInputState());

  const value: AppStateContextType = {
    // State
    jobId,
    jobStatus,
    results,
    error,
    simulationInput,
    pendingFile,
    inputValues,

    // Setters
    setJobId,
    setJobStatus,
    setResults,
    setError,
    setSimulationInput,
    setPendingFile,
    setInputValues,

    // Helper function
    initializeInputState,
  };

  return (
    <AppStateContext.Provider value={value}>
      {children}
    </AppStateContext.Provider>
  );
};

// ===========================================
// CUSTOM HOOK FOR USING CONTEXT
// ===========================================

/**
 * Hook to access the AppState context
 * @throws Error if used outside of AppStateProvider
 */
export const useAppState = () => {
  const context = useContext(AppStateContext);
  if (context === undefined) {
    throw new Error('useAppState must be used within an AppStateProvider');
  }
  return context;
};

