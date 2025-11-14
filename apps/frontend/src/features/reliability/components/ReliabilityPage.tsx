import React from 'react';
import Background from '../../../shared/components/Background';
import StatusIndicator from './StatusIndicator';
import ResultsDisplay from './ResultsDisplay';
import SelectionBar from '../../../shared/utilities/searchbar';
import { useAppState } from '../../../shared/contexts/AppStateContext';
import { useSimulation } from '../../../shared/hooks/useSimulation';
import { useFileUpload } from '../../../shared/hooks/useFileUpload';
import { useReliabilityFileUpload } from '../../../shared/hooks/useReliabilityFileUpload';

const ReliabilityPage: React.FC = () => {
  // Get state from Context
  const {
    jobId,
    jobStatus,
    results,
    error,
    simulationInput,
    pendingFile,
  } = useAppState();

  // Get simulation handlers from hook
  const { handleReset } = useSimulation();

  // Get file upload handlers from hooks
  const { handleFileSelect } = useFileUpload();
  const { handleReliabilityUpload } = useReliabilityFileUpload();

  const isLoading = !!jobId && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED';

  return (
    <>
      <Background />
      <SelectionBar
        width="300px" height="6.4%" shape="sharp-rectangle" x="150px" y="9.6%" color="bg-gray-800"
        onFileUpload={handleReliabilityUpload}
        pendingFile={pendingFile}
        onFileSelect={handleFileSelect}
      />

      {/* Main content area - positioned in the right panel */}
      <div
        style={{
          position: 'absolute',
          top: '12.8%',
          left: '300px',
          right: '2%',
          height: '87.2%',
          overflowY: 'auto',
          padding: '2rem',
          minWidth: '300px',
        }}
      >
        {results && (
          <ResultsDisplay
            results={results}
            onReset={handleReset}
            simulationInput={simulationInput}
          />
        )}

        {isLoading && <StatusIndicator jobId={jobId!} jobStatus={jobStatus!} />}

        {error && (
          <div style={{
            padding: '32px',
            backgroundColor: '#fee2e2',
            border: '1px solid #f87171',
            borderRadius: '8px',
            color: '#991b1b',
            textAlign: 'center'
          }}>
            <h3 style={{ fontWeight: 'bold', marginBottom: '8px' }}>An Error Occurred</h3>
            <p>{error}</p>
          </div>
        )}

        {!results && !isLoading && !error && (
          <div style={{ color: '#ffffff', textAlign: 'center' }}>
            <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>No Simulation Job Specified</h2>
            <p>Please start a new simulation or upload a result file.</p>
          </div>
        )}
      </div>
    </>
  );
};

export default ReliabilityPage;