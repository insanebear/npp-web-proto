import { useState } from 'react';
import Background from '../../../shared/components/Background';
import Menu, { RESULT_LABEL } from './menu';
import ResultsDisplay from './ResultsDisplay';
import StatusIndicator from './StatusIndicator';
import { TABS } from '../../../shared/constants/tabs';
import { getCodeKey } from '../../../shared/constants/labelToCode';
import { useAppState } from '../../../shared/contexts/AppStateContext';
import { useSimulation } from '../../../shared/hooks/useSimulation';
import { useFileSelect } from '../../../shared/hooks/useFileUpload';
import { useBayesianFileUpload } from '../../../shared/hooks/useBayesianFileUpload';
import { useReliabilityFileUpload } from '../../../shared/hooks/useReliabilityFileUpload';
import { useAppSettings } from '../../../shared/hooks/useAppSettings';
import { defaultSettings } from '../../../shared/contexts/AppSettingsContext';
import type { SettingsFormValues } from './SettingsForm';

function BayesianPage() {

  const {
    jobId,
    jobStatus,
    results,
    error: jobError,
    pendingFile,
    inputValues,
    setInputValues,
    simulationInput,
  } = useAppState();

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

  const [activeLabel, setActiveLabel] = useState('FP');

  const { handleStartSimulation, handleReset } = useSimulation();
  const { handleFileSelect } = useFileSelect();
  const { handleBayesianUpload } = useBayesianFileUpload(setSettingsValues);
  const { handleReliabilityUpload } = useReliabilityFileUpload(() => setActiveLabel(RESULT_LABEL));

  const handleInputChange = (key: string, value: string) => {
    setInputValues(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = () => {
    const payload = formatPayload(inputValues, settingsValues, workingDir);
    handleStartSimulation(payload);
    setActiveLabel(RESULT_LABEL);
  };

  const handleResetAndReturn = () => {
    handleReset();
    setActiveLabel('FP');
  };

  const activeLabelAndDropdowns = TABS.find(tab => tab.label === activeLabel);
  const isBusy = jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED';

  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      <Background />
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
        jobStatus={jobStatus}
        results={results}
      />

      {/* Analysis Result content — rendered outside Menu to use full main area */}
      {activeLabel === RESULT_LABEL && (
        <div style={{
          position: 'absolute',
          top: '64px',
          left: '300px',
          right: 0,
          bottom: 0,
          overflowY: 'auto',
          padding: '2rem',
        }}>
          {results ? (
            <ResultsDisplay
              results={results}
              onReset={handleResetAndReturn}
              simulationInput={simulationInput}
              jobId={jobId}
            />
          ) : isBusy && jobId ? (
            <StatusIndicator jobId={jobId} jobStatus={jobStatus!} />
          ) : jobError ? (
            <div style={{
              padding: '32px',
              backgroundColor: '#fee2e2',
              border: '1px solid #f87171',
              borderRadius: '8px',
              color: '#991b1b',
              textAlign: 'center',
            }}>
              <h3 style={{ fontWeight: 'bold', marginBottom: '8px' }}>An Error Occurred</h3>
              <p>{jobError}</p>
            </div>
          ) : (
            <div style={{ color: '#9CA3AF', textAlign: 'center', paddingTop: '20vh' }}>
              <p style={{ fontSize: '16px' }}>No results yet. Submit a job or load a result file.</p>
              <label style={{
                display: 'inline-block',
                marginTop: '16px',
                padding: '8px 16px',
                border: '1px solid #D1D5DB',
                borderRadius: '6px',
                backgroundColor: '#fff',
                color: '#374151',
                fontSize: '14px',
                cursor: 'pointer',
              }}>
                Load result file
                <input
                  type="file"
                  accept=".json"
                  style={{ display: 'none' }}
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (!file) return;
                    const reader = new FileReader();
                    reader.onload = (ev) => handleReliabilityUpload(ev.target?.result as string);
                    reader.readAsText(file);
                    e.target.value = '';
                  }}
                />
              </label>
            </div>
          )}
        </div>
      )}

      {/* Submit button */}
      <div style={{
        position: 'absolute',
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
          disabled={isBusy}
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
            backgroundColor: isBusy ? '#6b7280' : '#2563eb',
            cursor: isBusy ? 'not-allowed' : 'pointer',
          }}
          onMouseEnter={(e) => { if (!isBusy) e.currentTarget.style.backgroundColor = '#1d4ed8'; }}
          onMouseLeave={(e) => { if (!isBusy) e.currentTarget.style.backgroundColor = '#2563eb'; }}
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
