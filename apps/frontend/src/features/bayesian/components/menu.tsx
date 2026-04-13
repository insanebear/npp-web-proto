import Sidebar from "../../../shared/components/Sidebar";
import { RadioButtonGrid } from "./RadioButtonGrid";
import { TABS } from "../../../shared/constants/tabs";
import SettingsForm, { type SettingsFormValues } from "./SettingsForm";

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
}) => {
  const labels = ['Settings', ...TABS.map(tab => tab.label)];
  const labelSeparationPx = 48; // fixed spacing in pixels
  const firstButtonTopPx = 70; // fixed top offset for the first button

  return (
    <>
      {/* --- Left sidebar --- */}
      <Sidebar onFileUpload={onFileUpload} pendingFile={pendingFile} onFileSelect={onFileSelect}>
        {labels.map((label, index) => {
          const isActive = activeLabel === label;
          return (
            <button
              key={label}
              onClick={() => setActiveLabel(label)}
              style={{
                position: 'absolute',
                top: `${firstButtonTopPx + index * labelSeparationPx}px`,
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
                textAlign: 'left',
                transition: 'background-color 0.15s, color 0.15s',
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.backgroundColor = '#F3F4F6';
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              {label}
            </button>
          );
        })}
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
        {/* --- CONDITIONAL RENDERING: Settings, FP Input, or Dropdowns --- */}
        {activeLabel === 'Settings' ? (
          <div style={{ display: 'flex', justifyContent: 'center', paddingTop: '10vh' }}>
            <div style={{ width: '100%', maxWidth: '480px' }}>
              <SettingsForm values={settingsValues} onChange={onSettingsChange} />
            </div>
          </div>
        ) : activeLabel === 'FP' ? (
          // NEW: A dedicated positioning wrapper for the FP input
          <div style={{ 
              display: 'flex', 
              justifyContent: 'center', // Handles horizontal centering
              paddingTop: '20vh'        // Pushes the content down from the top by 20% of the viewport height
            }}>
            <div> {/* This inner div contains the actual input and label */}
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