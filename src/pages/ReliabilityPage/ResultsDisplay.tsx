// FILE: src/pages/ReliabilityPage/ResultsDisplay.tsx

import React from 'react';

interface ResultsDisplayProps {
  results: object;
  onReset: () => void;
  simulationInput: object | null;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, onReset, simulationInput }) => {

  const handleSaveResults = () => {
    if (!results) {
      alert("No results to save.");
      return;
    }

    const combinedData = {
      input: simulationInput,
      output: results,
    };

    const jsonString = JSON.stringify(combinedData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    a.download = `simulation-results-${timestamp}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div
      className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 p-6 bg-white rounded-lg shadow-2xl text-gray-800"
      style={{ width: '80%', maxWidth: '800px', height: '80%', display: 'flex', flexDirection: 'column' }}
    >
      <h2 className="text-2xl font-bold mb-4 text-center">Simulation Results</h2>
      <pre
        className="flex-grow bg-gray-100 p-4 rounded-md overflow-auto text-sm"
      >
        {JSON.stringify(results, null, 2)}
      </pre>
      <div className="mt-4 flex justify-center items-center gap-4">
        <button
          onClick={handleSaveResults}
          className="px-6 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-500 transition-colors"
          title="Save input and output to a JSON file"
        >
          Save Results
        </button>
        <button
          onClick={onReset}
          className="px-6 py-2 bg-sky-600 text-white font-semibold rounded-lg hover:bg-sky-500 transition-colors"
        >
          Start New Simulation
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;