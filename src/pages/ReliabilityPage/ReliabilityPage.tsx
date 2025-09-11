// FILE: src/pages/ReliabilityPage/ReliabilityPage.tsx

import React from 'react';
import Background from "../BayesianPage/background";
import StatusIndicator from './StatusIndicator';
import ResultsDisplay from './ResultsDisplay';
import SelectionBar from '../../utilities/searchbar';

interface ReliabilityPageProps {
  jobId: string | null;
  jobStatus: string | null;
  results: any | null;
  error: string | null;
  onReset: () => void;
  simulationInput: object | null;
  onFileUpload: (fileContent: string) => void;
  pendingFile: File | null;
  onFileSelect: (file: File) => void;
}

const ReliabilityPage: React.FC<ReliabilityPageProps> = ({ jobId, jobStatus, results, error, onReset, simulationInput, onFileUpload, pendingFile, onFileSelect }) => {
  const isLoading = !!jobId && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED';

  return (
    <>
      <Background />
      <SelectionBar
        width="25%" height="6.4%" shape="sharp-rectangle" x="12.5%" y="9.6%" color="bg-gray-800" scale={0.7}
        onFileUpload={onFileUpload}
        pendingFile={pendingFile}
        onFileSelect={onFileSelect}
      />

      {results && (
        <ResultsDisplay
          results={results}
          onReset={onReset}
          simulationInput={simulationInput}
        />
      )}

      {isLoading && <StatusIndicator jobId={jobId!} jobStatus={jobStatus!} />}

      {error && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 p-8 bg-red-100 border border-red-400 rounded-lg text-red-800 text-center">
          <h3 className="font-bold">An Error Occurred</h3>
          <p>{error}</p>
        </div>
      )}

      {!results && !isLoading && !error && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-white text-center">
          <h2 className="text-2xl">No Simulation Job Specified</h2>
          <p>Please start a new simulation or upload a result file.</p>
        </div>
      )}
    </>
  );
};

export default ReliabilityPage;