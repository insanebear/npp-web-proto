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

    // Remove __rawText from output before saving (it's only for display)
    const { __rawText, ...cleanOutput } = results as any;

    const combinedData = {
      input: simulationInput,
      output: cleanOutput,
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

  const renderResults = () => {
    if (!results) return null;

    // Display order for key metrics
    const displayOrder = {
      'PFD': 0,
      'SR_Total_Remained_Defect': 1,
      'SD_Total_Remained_Defect': 2,
      'IM_Total_Remained_Defect': 3,
      'ST_Total_Remained_Defect': 4,
      'IC_Total_Remained_Defect': 5
    } as Record<string, number>;
    
    // Support both shapes: metrics at root or nested under output
    const container: any = results as any;
    const metrics: any = (container && (container.PFD || container.SR_Total_Remained_Defect))
      ? container
      : (container && container.output);

    // Determine traces presence for summary label
    const hasTraces = Boolean((container && container.traces) || (metrics && metrics.traces));

    return (
      <div className="space-y-4">
        {metrics ? (
          <>
            <h3 className="text-lg font-semibold text-blue-800">Bayesian Simulation Results</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(metrics as Record<string, any>)
                // Hide non-metric keys from cards
                .filter(([param]) => param !== 'traces' && param !== '__rawText')
                .sort(([paramA], [paramB]) => {
                  const orderA = (displayOrder as any)[paramA] ?? 99;
                  const orderB = (displayOrder as any)[paramB] ?? 99;
                  return orderA - orderB;
                })
                .map(([param, data]: [string, any]) => (
                  <div key={param} className="bg-blue-50 p-4 rounded-lg border">
                    <h4 className="font-bold text-blue-900 mb-2">{param}</h4>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span>Mean:</span>
                        <span className="font-mono">{data?.mean !== undefined ? Number(data.mean).toFixed(6) : 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>SD:</span>
                        <span className="font-mono">{data?.sd !== undefined ? Number(data.sd).toFixed(6) : 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Median:</span>
                        <span className="font-mono">{data?.median !== undefined ? Number(data.median).toFixed(6) : 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>95% CI:</span>
                        <span className="font-mono text-xs">[
                          {data?.q2_5 !== undefined ? Number(data.q2_5).toFixed(6) : 'N/A'}, {data?.q97_5 !== undefined ? Number(data.q97_5).toFixed(6) : 'N/A'}
                        ]</span>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </>
        ) : (
          // Fallback: plain statistical output format
          <pre className="flex-grow bg-gray-100 p-4 rounded-md overflow-auto text-sm">
            {JSON.stringify(results, null, 2)}
          </pre>
        )}

        {/* Raw JSON viewer: prefer container raw text, then metrics raw text, then pretty-printed */}
        <details className="mt-4">
          <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">View Raw JSON Data{hasTraces ? ' (traces included)' : ''}</summary>
          <pre className="mt-2 bg-gray-100 p-4 rounded-md overflow-auto text-xs">{
            (container && container.__rawText)
              ?? (metrics && metrics.__rawText)
              ?? JSON.stringify(results, null, 2)
          }</pre>
        </details>
      </div>
    );
  };

  return (
    <div
      className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 p-6 bg-white rounded-lg shadow-2xl text-gray-800"
      style={{ width: '90%', maxWidth: '1200px', height: '85%', display: 'flex', flexDirection: 'column' }}
    >
      <h2 className="text-2xl font-bold mb-4 text-center">Simulation Results</h2>
      <div className="flex-grow overflow-auto">
        {renderResults()}
      </div>
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