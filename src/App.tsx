// FILE: src/App.tsx

import { useState, useEffect } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';

import BayesianPage from './pages/BayesianPage/BayesianPage';
import StatisticalPage from "./pages/StatisticalPage/StatisticalPage";
import SettingsPage from "./pages/SettingsPage/SettingsPage";
import ReliabilityPage from "./pages/ReliabilityPage/ReliabilityPage";

import { useAppSettings } from './hooks/useAppSettings';
import * as apiService from './services/apiService';
import { TABS } from './constants/tabs';

// ===========================================
// HELPER FUNCTIONS
// ===========================================

/**
 * Initialize or reset all input values to their default state
 * @param initialData - Optional data to pre-populate inputs
 * @returns Initial state object for input values
 */
const initializeInputState = (initialData?: any) => {
  const initialState: { [key: string]: string } = {};
  TABS.forEach(tab => {
    tab.children.forEach(child => {
      const key = `${tab.label}/${child.label}`;
      const uploadedValue = initialData?.[tab.label]?.[child.label];

      // Special handling for the new FP input
      if (tab.label === 'FP') {
        initialState[key] = uploadedValue || '56'; // Default FP to 56
      } else {
        // Use the uploaded value, or default to 'Medium' for dropdowns
        initialState[key] = uploadedValue || child.values[1];
      }
    });
  });
  return initialState;
};

// ===========================================
// MAIN APP COMPONENT
// ===========================================

function App() {
  const settingsProps = useAppSettings();
  const navigate = useNavigate();
  const location = useLocation();

  // ===========================================
  // STATE MANAGEMENT
  // ===========================================

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

  // ===========================================
  // SIMULATION EVENT HANDLERS
  // ===========================================

  /**
   * Start a new simulation with the provided form data
   * @param formData - The form data containing simulation parameters
   */
  const handleStartSimulation = async (formData: object) => {
    setError(null);
    setResults(null);
    setJobStatus('Submitting...');
    setSimulationInput(formData);
    try {
      const newJobId = await apiService.startSimulation(formData);
      setJobId(newJobId);
      navigate(`/reliability-views/${newJobId}`);
    } catch (err: any) {
      setError(err.message);
      setJobStatus(null);
    }
  };

  /**
   * Reset all application state to initial values
   */
  const handleReset = () => {
    setJobId(null);
    setJobStatus(null);
    setResults(null);
    setError(null);
    setSimulationInput(null);
    setPendingFile(null);
    setInputValues(initializeInputState());
    navigate('/');
  };

  // ===========================================
  // FILE UPLOAD HANDLERS
  // ===========================================

  /**
   * Handle file selection for upload
   * @param file - The selected file
   */
  const handleFileSelect = (file: File) => {
    setPendingFile(file);
  };

  /**
   * Handle file upload for Reliability page (results display)
   * @param fileContent - The content of the uploaded file
   */
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

  /**
   * Handle file upload for Bayesian page (input loading)
   * @param fileContent - The content of the uploaded file
   */
  const handleBayesianUpload = (fileContent: string) => {
    try {
      const data = JSON.parse(fileContent);
      if (typeof data === 'object' && data !== null && data.input && data.output) {
        setResults(data.output);
        setSimulationInput(data.input);
        const { settings } = data.input;
        if (settings) {
          settingsProps.setnChains(Number(settings.nChains));
          settingsProps.setnIter(Number(settings.nIter));
          settingsProps.setnBurnin(Number(settings.nBurnin));
          settingsProps.setnThin(Number(settings.nThin));
          settingsProps.setcomputeDIC(settings.computeDIC === 'true');
        }
        setInputValues(initializeInputState(data.input));
        setError(null);
        alert("Inputs and settings have been loaded from the file. Results are available on the Reliability Views page.");
        setPendingFile(null);
      } else {
        throw new Error("Invalid file. JSON must contain 'input' and 'output' keys.");
      }
    } catch (err: any) {
      setError(err.message || 'Failed to parse the uploaded file.');
    }
  };

  // ===========================================
  // INPUT MANAGEMENT HANDLERS
  // ===========================================

  /**
   * Update input values for any form input
   * @param key - The input key (tab/child format)
   * @param value - The new value
   */
  const handleInputChange = (key: string, value: string) => {
    setInputValues(prev => ({ ...prev, [key]: value }));
  };

  // ===========================================
  // SIDE EFFECTS
  // ===========================================

  // Job status polling effect
  useEffect(() => {
    if (!jobId || jobStatus === 'COMPLETED' || jobStatus === 'FAILED' || jobId === 'local') {
      return;
    }
    const intervalId = setInterval(async () => {
      try {
        const statusData = await apiService.getJobStatus(jobId);
        setJobStatus(statusData.jobStatus);
        if (statusData.jobStatus === 'FAILED') {
          setError('The simulation job failed.');
        }
      } catch (err) {
        setError('Failed to get job status.');
        setJobId(null);
      }
    }, 5000);
    return () => clearInterval(intervalId);
  }, [jobId, jobStatus]);

  // Results download effect
  useEffect(() => {
    if (jobStatus === 'COMPLETED' && jobId && jobId !== 'local') {
      apiService.getResults(jobId)
        .then(setResults)
        .catch(() => setError('Failed to fetch final results.'));
    }
  }, [jobStatus, jobId]);

  // URL job ID extraction effect
  useEffect(() => {
    const pathParts = location.pathname.split('/');
    const urlJobId = pathParts[2];
    if (pathParts[1] === 'reliability-views' && urlJobId && urlJobId !== 'local' && !jobId) {
      setJobId(urlJobId);
    }
  }, [location.pathname, jobId]);

  // ===========================================
  // COMPONENT RENDERING
  // ===========================================

  const BayesianPageComponent = (
    <BayesianPage
      settings={settingsProps}
      onStartSimulation={handleStartSimulation}
      jobError={error}
      jobStatus={jobStatus}
      onFileUpload={handleBayesianUpload}
      pendingFile={pendingFile}
      onFileSelect={handleFileSelect}
      inputValues={inputValues}
      onInputChange={handleInputChange}
    />
  );

  return (
    <Routes>
      <Route path="/" element={BayesianPageComponent} />
      <Route path="/bayesian" element={BayesianPageComponent} />
      <Route path="/statistical" element={<StatisticalPage />} />
      <Route path="/settings" element={<SettingsPage {...settingsProps}/>} />
      <Route
        path="/reliability-views/:jobId?"
        element={
          <ReliabilityPage
            jobId={jobId}
            jobStatus={jobStatus}
            results={results}
            error={error}
            onReset={handleReset}
            simulationInput={simulationInput}
            onFileUpload={handleReliabilityUpload}
            pendingFile={pendingFile}
            onFileSelect={handleFileSelect}
          />
        }
      />
    </Routes>
  );
}

export default App;