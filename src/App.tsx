// FILE: src/App.tsx

import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';

import BayesianPage from './pages/BayesianPage/BayesianPage';
import StatisticalPage from "./pages/StatisticalPage/StatisticalPage";
import SettingsPage from "./pages/SettingsPage/SettingsPage";
import ReliabilityPage from "./pages/ReliabilityPage/ReliabilityPage";

import { useAppSettings } from './hooks/useAppSettings';
import * as apiService from './services/apiService';

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
  const [initialBayesianValues, setInitialBayesianValues] = useState<object | null>(null);
  const [pendingFile, setPendingFile] = useState<File | null>(null);


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
    setInitialBayesianValues(null);
    setPendingFile(null); // Also clear any pending file on reset
    navigate('/');
  };

  const handleFileSelect = (file: File) => {
    setPendingFile(file);
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
            setInitialBayesianValues(data.input);
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
  return (
    <Routes>
      <Route
        path="/"
        element={
          <BayesianPage
            settings={settingsProps}
            onStartSimulation={handleStartSimulation}
            jobError={error}
            isSubmitting={!!jobStatus && jobStatus === 'Submitting...'}
            onFileUpload={handleBayesianUpload}
            initialValues={initialBayesianValues}
            pendingFile={pendingFile}
            onFileSelect={handleFileSelect}
          />
        }
      />
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