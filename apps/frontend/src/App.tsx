// FILE: src/App.tsx

import { useAppState } from './shared/contexts/AppStateContext';
import { Routes, Route } from 'react-router-dom';
import { useSimulation } from './shared/hooks/useSimulation';
import { useFileUpload } from './shared/hooks/useFileUpload';
import { useReliabilityFileUpload } from './shared/hooks/useReliabilityFileUpload';
import { useBayesianFileUpload } from './shared/hooks/useBayesianFileUpload';

import BayesianPage from './pages/BayesianPage/BayesianPage';
import StatisticalPage from "./pages/StatisticalPage/StatisticalPage";
import SettingsPage from "./pages/SettingsPage/SettingsPage";
import ReliabilityPage from "./pages/ReliabilityPage/ReliabilityPage";

import { useAppSettings } from './hooks/useAppSettings'; 

// ===========================================
// MAIN APP COMPONENT
// ===========================================

function App() {
  const settingsProps = useAppSettings();
  // ===========================================
  // STATE MANAGEMENT
  // ===========================================

  // Get state from Context
  const {
    jobId,
    jobStatus,
    results,
    error,
    simulationInput,
    pendingFile,
    inputValues,
    setInputValues
  } = useAppState();

  // Get simulation handlers from hook
  const { handleStartSimulation, handleReset } = useSimulation();

  // Get file upload handlers from hooks
  const { handleFileSelect } = useFileUpload();
  const { handleReliabilityUpload } = useReliabilityFileUpload();
  const { handleBayesianUpload } = useBayesianFileUpload();

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
      <Route path="/settings" element={<SettingsPage/>} />
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