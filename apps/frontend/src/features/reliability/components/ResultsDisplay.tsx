import React from 'react';
import type { SimulationResults, SimulationInput, SimulationOutput } from '../../../shared/types';
import { getDownloadPresignedUrl } from '../../../shared/services/apiService';

interface ResultsDisplayProps {
  results: SimulationResults;
  onReset: () => void;
  simulationInput: SimulationInput | null;
  /** BBN inference job ID — used to derive the .nc trace file key for download */
  jobId?: string | null;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, onReset, simulationInput, jobId }) => {

  const triggerDownload = (url: string, filename: string) => {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const downloadJson = (filename: string, jsonString: string) => {
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    triggerDownload(url, filename);
    URL.revokeObjectURL(url);
  };

  const handleSaveResults = async () => {
    if (!results) {
      alert("No results to save.");
      return;
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const jsonFilename = `simulation-results-${timestamp}.json`;

    // Build JSON string
    let jsonString: string;
    if (results.input && results.output) {
      const { __rawText, ...cleanResults } = results;
      jsonString = JSON.stringify(cleanResults, null, 2);
    } else {
      const { __rawText, ...cleanOutput } = results;
      jsonString = JSON.stringify({ input: simulationInput, output: cleanOutput }, null, 2);
    }

    // Download JSON
    downloadJson(jsonFilename, jsonString);

    // Download NC trace if jobId is available
    if (jobId) {
      const ncKey = `results/bbn/prior-trace-${jobId}.nc`;
      const ncFilename = `prior-trace-${jobId}.nc`;
      try {
        const { download_url } = await getDownloadPresignedUrl(ncKey);
        triggerDownload(download_url, ncFilename);
      } catch (err) {
        console.warn('NC trace file not available for download:', err);
        // NC download is best-effort — don't block JSON download
      }
    }
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
    
    // Support both shapes: complete JSON (input + output) or output-only format
    // TODO: Confirm whether output-only payloads still occur. If not, simplify this path.
    const isSimulationOutput = (data: SimulationResults | SimulationOutput): data is SimulationOutput => {
      if (!data || typeof data !== 'object') return false;
      const maybe = data as SimulationOutput;
      return Boolean(
        maybe.PFD ||
        maybe.SR_Total_Remained_Defect ||
        maybe.SD_Total_Remained_Defect ||
        maybe.IM_Total_Remained_Defect ||
        maybe.ST_Total_Remained_Defect ||
        maybe.IC_Total_Remained_Defect
      );
    };

    const metrics: SimulationOutput | undefined = (() => {
      if (results.input && results.output) {
        return results.output;
      }
      if (results.output) {
        return results.output;
      }
      if (isSimulationOutput(results)) {
        return results;
      }
      return undefined;
    })();

    const hasTraces = Boolean(metrics?.traces);
    const rawJsonText =
      results.__rawText ??
      metrics?.__rawText ??
      JSON.stringify(results, null, 2);

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {metrics ? (
          <>
            <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1e40af' }}>Bayesian Simulation Results</h3>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
              gap: '16px' 
            }}>
              {Object.entries(metrics as Record<string, any>)
                // Hide non-metric keys from cards
                .filter(([param]) => param !== 'traces' && param !== '__rawText')
                .sort(([paramA], [paramB]) => {
                  const orderA = (displayOrder as any)[paramA] ?? 99;
                  const orderB = (displayOrder as any)[paramB] ?? 99;
                  return orderA - orderB;
                })
                .map(([param, data]: [string, any]) => (
                  <div key={param} style={{
                    backgroundColor: '#eff6ff',
                    padding: '16px',
                    borderRadius: '8px',
                    border: '1px solid #dbeafe'
                  }}>
                    <h4 style={{ fontWeight: 'bold', color: '#1e3a8a', marginBottom: '8px' }}>{param}</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '14px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>Mean:</span>
                        <span style={{ fontFamily: 'monospace' }}>{data?.mean !== undefined ? Number(data.mean).toFixed(6) : 'N/A'}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>SD:</span>
                        <span style={{ fontFamily: 'monospace' }}>{data?.sd !== undefined ? Number(data.sd).toFixed(6) : 'N/A'}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>Median:</span>
                        <span style={{ fontFamily: 'monospace' }}>{data?.median !== undefined ? Number(data.median).toFixed(6) : 'N/A'}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>95% CI:</span>
                        <span style={{ fontFamily: 'monospace', fontSize: '12px' }}>[
                          {data?.q2_5 !== undefined ? Number(data.q2_5).toFixed(6) : 'N/A'}, {data?.q97_5 !== undefined ? Number(data.q97_5).toFixed(6) : 'N/A'}
                        ]</span>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </>
        ) : (
          <pre style={{
            flexGrow: 1,
            backgroundColor: '#f3f4f6',
            padding: '16px',
            borderRadius: '6px',
            overflow: 'auto',
            fontSize: '14px'
          }}>
            {JSON.stringify(results, null, 2)}
          </pre>
        )}

        <details style={{ marginTop: '16px' }}>
          <summary style={{ 
            cursor: 'pointer', 
            fontSize: '14px', 
            color: '#4b5563',
            textDecoration: 'underline'
          }}>
            View Raw JSON Data{hasTraces ? ' (traces included)' : ''}
          </summary>
          <pre
            style={{
              marginTop: '8px',
              backgroundColor: '#f3f4f6',
              padding: '16px',
              borderRadius: '6px',
              overflow: 'auto',
              fontSize: '12px'
            }}
          >
            {rawJsonText}
          </pre>
        </details>
      </div>
    );
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '24px',
        backgroundColor: '#ffffff',
        borderRadius: '8px',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        color: '#1f2937',
        width: '90%',
        maxWidth: '1200px',
        height: '85%',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      <h2 style={{ 
        fontSize: '24px', 
        fontWeight: 'bold', 
        marginBottom: '16px', 
        textAlign: 'center' 
      }}>
        Simulation Results
      </h2>
      <div style={{ flexGrow: 1, overflow: 'auto' }}>
        {renderResults()}
      </div>
      <div style={{ 
        marginTop: '16px', 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        gap: '16px' 
      }}>
        <button
          onClick={handleSaveResults}
          style={{
            padding: '8px 24px',
            backgroundColor: '#059669',
            color: '#ffffff',
            fontWeight: '600',
            borderRadius: '8px',
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#047857'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#059669'}
          title={jobId ? "Download JSON result + NC trace file" : "Save input and output to a JSON file"}
        >
          Download Results{jobId ? ' (JSON + NC)' : ''}
        </button>
        <button
          onClick={onReset}
          style={{
            padding: '8px 24px',
            backgroundColor: '#0284c7',
            color: '#ffffff',
            fontWeight: '600',
            borderRadius: '8px',
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#0369a1'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0284c7'}
        >
          Start New Simulation
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;