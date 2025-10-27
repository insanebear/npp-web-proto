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

// Helper function to initialize or reset all input values
const initializeInputState = (initialData?: any) => {
  const initialState: { [key: string]: string } = {};
  TABS.forEach(tab => {
    tab.children.forEach(child => {
      const key = `${tab.label}/${child.label}`;
      const uploadedValue = initialData?.[tab.label]?.[child.label];

      // Special handling for the new FP input
      if (tab.label === 'FP') {
        initialState[key] = uploadedValue || '120'; // Default FP to 120
      } else {
        // Use the uploaded value, or default to 'Medium' for dropdowns
        initialState[key] = uploadedValue || child.values[1];
      }
    });
  });
  return initialState;
};

function App() {
  const settingsProps = useAppSettings();
  const navigate = useNavigate();
  const location = useLocation();

  // --- Central State Management ---
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [results, setResults] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [simulationInput, setSimulationInput] = useState<object | null>(null);
  const [pendingFile, setPendingFile] = useState<File | null>(null);

  // UNIFIED STATE: State for all inputs is now managed centrally.
  const [inputValues, setInputValues] = useState(() => initializeInputState());


  // --- Core Functions ---

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

  const handleReset = () => {
    setJobId(null);
    setJobStatus(null);
    setResults(null);
    setError(null);
    setSimulationInput(null);
    setPendingFile(null); // Also clear any pending file on reset
    // Also reset all inputs to their default values
    setInputValues(initializeInputState());
    navigate('/');
  };

  const handleFileSelect = (file: File) => {
    setPendingFile(file);
  };

  // UNIFIED STATE HANDLER: This function updates the central state for any input.
  const handleInputChange = (key: string, value: string) => {
    setInputValues(prev => ({ ...prev, [key]: value }));
  };

  // --- Upload Handlers for Different Pages ---

  const handleReliabilityUpload = (fileContent: string) => {
    try {
      const data = JSON.parse(fileContent);
      if (typeof data === 'object' && data !== null && 'output' in data) {
        setResults(data.output);
        setSimulationInput(data.input || null);
        setJobId('local');
        setJobStatus('COMPLETED');
        setError(null);
        navigate('/reliability-views/local');
        setPendingFile(null); // Clear the pending file after successful upload
      } else {
        throw new Error("Invalid file. JSON must contain an 'output' key.");
      }
    } catch (err: any) {
      setError(err.message || 'Failed to parse the uploaded file.');
    }
  };

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
            // When a file is uploaded, update the input state with its values
            setInputValues(initializeInputState(data.input));
            setError(null);
            alert("Inputs and settings have been loaded from the file. Results are available on the Reliability Views page.");
            setPendingFile(null); // Clear the pending file after successful upload
        } else {
            throw new Error("Invalid file. JSON must contain 'input' and 'output' keys.");
        }
    } catch (err: any) {
        setError(err.message || 'Failed to parse the uploaded file.');
    }
  };


  // --- useEffect Hooks for State Synchronization ---

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

  useEffect(() => {
    if (jobStatus === 'COMPLETED' && jobId && jobId !== 'local') {
      apiService.getResults(jobId)
        .then(setResults)
        .catch(() => setError('Failed to fetch final results.'));
    }
  }, [jobStatus, jobId]);

  useEffect(() => {
    const pathParts = location.pathname.split('/');
    const urlJobId = pathParts[2];
    if (pathParts[1] === 'reliability-views' && urlJobId && urlJobId !== 'local' && !jobId) {
      setJobId(urlJobId);
    }
  }, [location.pathname, jobId]);


  // --- Component Routing ---
  const BayesianPageComponent = (
    <BayesianPage
      settings={settingsProps}
      onStartSimulation={handleStartSimulation}
      jobError={error}
      jobStatus={jobStatus}
      onFileUpload={handleBayesianUpload}
      pendingFile={pendingFile}
      onFileSelect={handleFileSelect}
      // Pass the unified state and handler function as props
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