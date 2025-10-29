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
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          padding: '16px',
          backgroundColor: '#fee2e2',
          color: '#991b1b',
          borderRadius: '6px'
        }}>
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
        top: '80px', 
        width: '340px', 
        maxWidth: 'calc(100vw - 50% - 150px - 40px)',
        height: '60px',
        padding: '12px 16px',
        zIndex: 10
      }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '24px', 
          height: '100%' 
        }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '12px' 
          }}>
            <label style={{ 
              color: '#000000', 
              fontSize: '14px', 
              fontWeight: '500', 
              whiteSpace: 'nowrap' 
            }}>
              Include trace raw data
            </label>
            <input
              type="checkbox"
              checked={includeTraceData}
              onChange={(e) => setIncludeTraceData(e.target.checked)}
              style={{
                width: '16px',
                height: '16px',
                color: '#2563eb',
                backgroundColor: '#f3f4f6',
                borderColor: '#d1d5db',
                borderRadius: '4px',
                outline: 'none'
              }}
            />
          </div>
          <button
            onClick={handleSubmit}
            disabled={jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED'}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              fontWeight: '600',
              color: '#ffffff',
              fontSize: '14px',
              transition: 'all 0.3s ease-in-out',
              border: '2px solid transparent',
              width: '120px',
              height: '36px',
              backgroundColor: jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED' 
                ? '#6b7280' 
                : '#b91c1c',
              cursor: jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED' 
                ? 'not-allowed' 
                : 'pointer'
            }}
            onMouseEnter={(e) => {
              if (jobStatus === null || jobStatus === 'COMPLETED' || jobStatus === 'FAILED') {
                e.currentTarget.style.backgroundColor = '#dc2626';
              }
            }}
            onMouseLeave={(e) => {
              if (jobStatus === null || jobStatus === 'COMPLETED' || jobStatus === 'FAILED') {
                e.currentTarget.style.backgroundColor = '#b91c1c';
              }
            }}
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