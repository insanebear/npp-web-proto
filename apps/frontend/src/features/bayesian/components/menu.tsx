import Sidebar from "../../../shared/components/Sidebar";
import { RadioButtonGrid } from "./RadioButtonGrid";
import { TABS } from "../../../shared/constants/tabs";
import SettingsForm, { type SettingsFormValues } from "./SettingsForm";
import type { SimulationResults } from "../../../shared/types";

const RESULT_LABEL = 'Analysis Result';

const getResultDotColor = (jobStatus: string | null, results: SimulationResults | null) => {
  if (jobStatus === 'COMPLETED' || results) return '#059669'; // green
  if (jobStatus === 'FAILED') return '#dc2626';              // red
  if (jobStatus !== null) return '#f59e0b';                  // orange (running)
  return '#9CA3AF';                                          // gray (no job)
};

const Menu = ({
  activeLabel,
  setActiveLabel,
  inputValues,
  onInputChange,
  activeLabelAndDropdowns,
  onFileUpload,
  pendingFile,
  onFileSelect,
  settingsValues,
  onSettingsChange,
  jobStatus,
  results,
}: {
  activeLabel: string;
  setActiveLabel: (label: string) => void;
  inputValues: any;
  onInputChange: (key: string, value: string) => void;
  activeLabelAndDropdowns: any;
  onFileUpload: any;
  pendingFile: any;
  onFileSelect: any;
  settingsValues: SettingsFormValues;
  onSettingsChange: (key: keyof SettingsFormValues, value: number) => void;
  jobStatus: string | null;
  results: SimulationResults | null;
}) => {
  const labels = ['Settings', ...TABS.map(tab => tab.label)];
  const labelSeparationPx = 48;
  const firstButtonTopPx = 70;

  const dotColor = getResultDotColor(jobStatus, results);
  const isResultActive = activeLabel === RESULT_LABEL;

  const navButtonStyle = (isActive: boolean) => ({
    position: 'absolute' as const,
    left: 0,
    width: '300px',
    height: '44px',
    display: 'flex',
    alignItems: 'center',
    paddingLeft: '20px',
    border: 'none',
    borderLeft: isActive ? '3px solid #2563eb' : '3px solid transparent',
    backgroundColor: isActive ? '#EFF6FF' : 'transparent',
    color: isActive ? '#2563eb' : '#4B5563',
    fontSize: '14px',
    fontWeight: isActive ? '600' : '500',
    borderRadius: '0',
    cursor: 'pointer',
    textAlign: 'left' as const,
    transition: 'background-color 0.15s, color 0.15s',
  });

  return (
    <>
      {/* --- Left sidebar --- */}
      <Sidebar onFileUpload={onFileUpload} pendingFile={pendingFile} onFileSelect={onFileSelect}>
        {/* Input tabs */}
        {labels.map((label, index) => {
          const isActive = activeLabel === label;
          return (
            <button
              key={label}
              onClick={() => setActiveLabel(label)}
              style={{ ...navButtonStyle(isActive), top: `${firstButtonTopPx + index * labelSeparationPx}px` }}
              onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.backgroundColor = '#F3F4F6'; }}
              onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.backgroundColor = 'transparent'; }}
            >
              {label}
            </button>
          );
        })}

        {/* Separator */}
        <div style={{
          position: 'absolute',
          bottom: '60px',
          left: '12px',
          right: '12px',
          height: '1px',
          backgroundColor: '#E5E7EB',
        }} />

        {/* Analysis Result button */}
        <button
          onClick={() => setActiveLabel(RESULT_LABEL)}
          style={{
            ...navButtonStyle(isResultActive),
            position: 'absolute',
            bottom: '10px',
            gap: '8px',
          }}
          onMouseEnter={(e) => { if (!isResultActive) e.currentTarget.style.backgroundColor = '#F3F4F6'; }}
          onMouseLeave={(e) => { if (!isResultActive) e.currentTarget.style.backgroundColor = 'transparent'; }}
        >
          <span style={{
            width: '8px', height: '8px', borderRadius: '50%',
            backgroundColor: dotColor, flexShrink: 0,
          }} />
          {RESULT_LABEL}
        </button>
      </Sidebar>

      {/* --- Main container for the right-side inputs --- */}
      <div
        style={{
          position: 'absolute',
          top: '160px',
          left: '300px',
          right: '2%',
          minHeight: '87.2%',
          padding: '2rem',
          minWidth: '300px',
          overflow: 'visible',
        }}
      >
        {activeLabel === 'Settings' ? (
          <div style={{ display: 'flex', justifyContent: 'center', paddingTop: '10vh' }}>
            <div style={{ width: '100%', maxWidth: '480px' }}>
              <SettingsForm values={settingsValues} onChange={onSettingsChange} />
            </div>
          </div>
        ) : activeLabel === 'FP' ? (
          <div style={{ display: 'flex', justifyContent: 'center', paddingTop: '20vh' }}>
            <div>
              {activeLabelAndDropdowns?.children.map((child: any) => {
                const key = `FP/${child.label}`;
                return (
                  <div key={key}>
                    <label htmlFor={key} style={{ color: '#4B5563', display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '14px' }}>
                      {child.label}
                    </label>
                    <input
                      id={key}
                      type="number"
                      value={inputValues[key] || ''}
                      onChange={(e) => onInputChange(key, e.target.value)}
                      style={{
                        padding: '8px 12px',
                        borderRadius: '6px',
                        border: '1px solid #D1D5DB',
                        width: '100%',
                        maxWidth: '400px',
                        fontSize: '14px',
                        backgroundColor: '#FFFFFF',
                        color: '#111827',
                      }}
                    />
                  </div>
                );
              })}
            </div>
          </div>
        ) : activeLabel === RESULT_LABEL ? (
          null /* rendered by BayesianPage */
        ) : (
          <RadioButtonGrid
            children={activeLabelAndDropdowns?.children ?? []}
            tabLabel={activeLabelAndDropdowns?.label ?? ''}
            inputValues={inputValues}
            onInputChange={onInputChange}
          />
        )}
      </div>
    </>
  );
}

export default Menu;
export { RESULT_LABEL };
