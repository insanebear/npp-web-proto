import { useState } from 'react';
import Background from '../../../shared/components/Background';
import Menu from './menu';
import { TABS } from '../../../shared/constants/tabs';
import { getCodeKey } from '../../../shared/constants/labelToCode';
import { useAppState } from '../../../shared/contexts/AppStateContext';
import { useSimulation } from '../../../shared/hooks/useSimulation';
import { useFileSelect } from '../../../shared/hooks/useFileUpload';
import { useBayesianFileUpload } from '../../../shared/hooks/useBayesianFileUpload';
import { useAppSettings } from '../../../shared/hooks/useAppSettings';
import { defaultSettings } from '../../../shared/contexts/AppSettingsContext';
import type { SettingsFormValues } from './SettingsForm';

function BayesianPage() {

  // Get state from Context
  const {
    jobStatus,
    error: jobError,
    pendingFile,
    inputValues,
    setInputValues,
  } = useAppState();

  // workingDir from context; hyperparameter fields managed locally
  const { workingDir } = useAppSettings();

  const [settingsValues, setSettingsValues] = useState<SettingsFormValues>({
    nChains: defaultSettings.nChains,
    nIter: defaultSettings.nIter,
    nBurnin: defaultSettings.nBurnin,
    nThin: defaultSettings.nThin,
  });

  const handleSettingsChange = (key: keyof SettingsFormValues, value: number) => {
    setSettingsValues(prev => ({ ...prev, [key]: value }));
  };

  // Get handlers from hooks
  const { handleStartSimulation } = useSimulation();
  const { handleFileSelect } = useFileSelect();
  const { handleBayesianUpload } = useBayesianFileUpload(setSettingsValues);

  // Input change handler
  const handleInputChange = (key: string, value: string) => {
    setInputValues(prev => ({ ...prev, [key]: value }));
  };

  // The active tab state remains local. We'll default to the new "FP" tab.
  const [activeLabel, setActiveLabel] = useState('FP');

  const handleSubmit = () => {
    const payload = formatPayload(inputValues, settingsValues, workingDir);
    handleStartSimulation(payload);
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
        inputValues={inputValues}
        onInputChange={handleInputChange}
        activeLabelAndDropdowns={activeLabelAndDropdowns}
        onFileUpload={handleBayesianUpload}
        pendingFile={pendingFile}
        onFileSelect={handleFileSelect}
        settingsValues={settingsValues}
        onSettingsChange={handleSettingsChange}
      />
      {/* Fixed-width control box positioned below Settings */}
      <div className="absolute" style={{
        right: '40px',
        top: '80px',
        height: '60px',
        padding: '12px 16px',
        zIndex: 10,
        display: 'flex',
        alignItems: 'center',
      }}>
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
                : '#2563eb',
              cursor: jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED' 
                ? 'not-allowed' 
                : 'pointer'
            }}
            onMouseEnter={(e) => {
              if (jobStatus === null || jobStatus === 'COMPLETED' || jobStatus === 'FAILED') {
                e.currentTarget.style.backgroundColor = '#1d4ed8';
              }
            }}
            onMouseLeave={(e) => {
              if (jobStatus === null || jobStatus === 'COMPLETED' || jobStatus === 'FAILED') {
                e.currentTarget.style.backgroundColor = '#2563eb';
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
  );
}

const formatPayload = (values: { [key: string]: string }, settings: SettingsFormValues, workingDir: string) => {
  const payload: { [key: string]: any } = {};
  for (const key in values) {
    const [tabLabel, childLabel] = key.split('/');
    if (!payload[tabLabel]) {
      payload[tabLabel] = {};
    }
    const codeKey = getCodeKey(tabLabel, childLabel);
    const outKey = codeKey || childLabel;
    payload[tabLabel][outKey] = values[key];
  }

  payload['settings'] = {
    nChains: String(settings.nChains),
    nIter: String(settings.nIter),
    nBurnin: String(settings.nBurnin),
    nThin: String(settings.nThin),
    workingDir,
  };
  return payload;
};

export default BayesianPage;