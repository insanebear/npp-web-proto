// FILE: src/pages/BayesianPage/BayesianPage.tsx

import { useState } from 'react';
import Background from './background';
import Menu from './menu';
import { TABS } from '../../constants/tabs';

// All props are now passed down from App.tsx
function BayesianPage({
  settings,
  onStartSimulation,
  jobStatus,
  jobError,
  onFileUpload,
  pendingFile,
  onFileSelect,
  inputValues,
  onInputChange
}: any) {
  // The active tab state remains local. We'll default to the new "FP" tab.
  const [activeLabel, setActiveLabel] = useState('FP');
  const [includeTraceData, setIncludeTraceData] = useState(false);

  const handleSubmit = () => {
    // The `inputValues` from props now contains FP and all dropdowns.
    const payload = formatPayload(inputValues, settings);
    // Include trace data setting in the payload
    payload.settings.includeTraceData = includeTraceData;
    onStartSimulation(payload);
  };

  const activeLabelAndDropdowns = TABS.find(tab => tab.label === activeLabel);

  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      <Background />
      {jobError && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 p-4 bg-red-100 text-red-800 rounded-md">
          Error: {jobError}
        </div>
      )}
      <Menu
        activeLabel={activeLabel}
        setActiveLabel={setActiveLabel}
        inputValues={inputValues} // Pass unified state down
        onInputChange={onInputChange} // Pass unified handler down
        activeLabelAndDropdowns={activeLabelAndDropdowns}
        onFileUpload={onFileUpload}
        pendingFile={pendingFile}
        onFileSelect={onFileSelect}
      />
      {/* Fixed-width control box positioned below Settings */}
      <div className="absolute" style={{ 
        right: '40px',
        top: '68px', 
        width: '340px', 
        maxWidth: 'calc(100vw - 50% - 150px - 40px)',
        height: '60px',
        padding: '12px 16px',
        zIndex: 10
      }}>
        <div className="flex items-center gap-6 h-full">
          <div className="flex items-center gap-3">
            <label className="text-black text-sm font-medium whitespace-nowrap">
              Include trace raw data
            </label>
            <input
              type="checkbox"
              checked={includeTraceData}
              onChange={(e) => setIncludeTraceData(e.target.checked)}
              className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
            />
          </div>
          <button
            onClick={handleSubmit}
            disabled={jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED'}
            className={`
              px-4 py-2 rounded-lg font-semibold text-white text-sm
              transition-all duration-300 ease-in-out border-2 border-transparent
              ${jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED' 
                ? 'bg-gray-500 cursor-not-allowed' 
                : 'bg-red-700 hover:bg-red-600 active:bg-red-800 cursor-pointer'
              }
            `}
            style={{ width: '120px', height: '36px' }}
          >
            {!jobStatus || jobStatus === 'COMPLETED' || jobStatus === 'FAILED' 
              ? 'Submit' 
              : `${jobStatus.charAt(0).toUpperCase() + jobStatus.slice(1).toLowerCase()}...`
            }
          </button>
        </div>
      </div>
    </div>
  );
}

// This function now works generically for all inputs, including FP.
const formatPayload = (values: { [key: string]: string }, settings: any) => {
  const payload: { [key: string]: any } = {};
  for (const key in values) {
    const [tabLabel, childLabel] = key.split('/');
    if (!payload[tabLabel]) {
      payload[tabLabel] = {};
    }
    payload[tabLabel][childLabel] = values[key];
  }
  // No longer needed: payload['FP'] = { 'FP Input': '120' };
  payload['settings'] = {
    nChains: String(settings.nChains),
    nIter: String(settings.nIter),
    nBurnin: String(settings.nBurnin),
    nThin: String(settings.nThin),
    computeDIC: String(settings.computeDIC),
    workingDir: settings.workingDir,
  };
  return payload;
};

export default BayesianPage;