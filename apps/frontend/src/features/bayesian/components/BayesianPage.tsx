import { useRef, useState } from 'react';
import Background from '../../../shared/components/Background';
import Menu, { RESULT_LABEL } from './menu';
import ResultsDisplay from './ResultsDisplay';
import StatusIndicator from './StatusIndicator';
import { TABS } from '../../../shared/constants/tabs';
import { getCodeKey } from '../../../shared/constants/labelToCode';
import { useAppState } from '../../../shared/contexts/AppStateContext';
import { useSimulation } from '../../../shared/hooks/useSimulation';
import { useBayesianFileUpload } from '../../../shared/hooks/useBayesianFileUpload';

import { useAppSettings } from '../../../shared/hooks/useAppSettings';
import { defaultSettings } from '../../../shared/contexts/AppSettingsContext';
import type { SettingsFormValues } from './SettingsForm';

const TOP_BAR_HEIGHT = 52;

function BayesianPage() {

  const {
    jobId,
    jobStatus,
    results,
    error: jobError,
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

  const [activeLabel, setActiveLabel] = useState('FP');
  const [loadedFileName, setLoadedFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { handleStartSimulation, handleReset } = useSimulation();
  const { handleBayesianUpload } = useBayesianFileUpload(setSettingsValues);

  const handleSettingsChange = (key: keyof SettingsFormValues, value: number) => {
    setSettingsValues(prev => ({ ...prev, [key]: value }));
  };

  const handleInputChange = (key: string, value: string) => {
    setInputValues(prev => ({ ...prev, [key]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoadedFileName(file.name);
    const reader = new FileReader();
    reader.onload = (ev) => handleBayesianUpload(ev.target?.result as string);
    reader.readAsText(file);
    e.target.value = '';
  };

  const handleSubmit = () => {
    const payload = formatPayload(inputValues, settingsValues, workingDir);
    handleStartSimulation(payload);
    setActiveLabel(RESULT_LABEL);
  };

  const handleResetAndReturn = () => {
    handleReset();
    setLoadedFileName(null);
    setActiveLabel('FP');
  };

  const activeLabelAndDropdowns = TABS.find(tab => tab.label === activeLabel);
  const isBusy = jobStatus !== null && jobStatus !== 'COMPLETED' && jobStatus !== 'FAILED';
  const isResultTab = activeLabel === RESULT_LABEL;

  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      <Background />
      <Menu
        activeLabel={activeLabel}
        setActiveLabel={setActiveLabel}
        inputValues={inputValues}
        onInputChange={handleInputChange}
        activeLabelAndDropdowns={activeLabelAndDropdowns}
        settingsValues={settingsValues}
        onSettingsChange={handleSettingsChange}
        jobStatus={jobStatus}
        results={results}
      />

      {/* Top bar: file upload + submit */}
      <div style={{
        position: 'absolute',
        top: '64px',
        left: '300px',
        right: 0,
        height: `${TOP_BAR_HEIGHT}px`,
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #E5E7EB',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 20px',
        zIndex: 10,
      }}>
        {/* File upload */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            style={{
              padding: '5px 12px',
              fontSize: '14px',
              fontWeight: '500',
              border: '1px solid #D1D5DB',
              borderRadius: '6px',
              backgroundColor: '#fff',
              color: '#374151',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'background-color 0.15s, border-color 0.15s',
            }}
            onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#F3F4F6'; e.currentTarget.style.borderColor = '#9CA3AF'; }}
            onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#fff'; e.currentTarget.style.borderColor = '#D1D5DB'; }}
          >
            Choose file
          </button>
          <span style={{
            fontSize: '13px',
            color: loadedFileName ? '#374151' : '#9CA3AF',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            maxWidth: '300px',
          }}>
            {loadedFileName ?? 'No file chosen'}
          </span>
        </div>

        {/* Submit button — hidden on Analysis Result tab */}
        {!isResultTab && (
          <button
            onClick={handleSubmit}
            disabled={isBusy}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              fontWeight: '600',
              color: '#ffffff',
              fontSize: '14px',
              transition: 'background-color 0.2s',
              border: 'none',
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
        )}
      </div>

      {/* Main content area */}
      {isResultTab ? (
        <div style={{
          position: 'absolute',
          top: `${64 + TOP_BAR_HEIGHT}px`,
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
              <p style={{ fontSize: '16px' }}>No results yet. <br/> <br/>Submit a new software development quality assessment <br/> or load a previous assessment file.</p>
            </div>
          )}
        </div>
      ) : null}
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
