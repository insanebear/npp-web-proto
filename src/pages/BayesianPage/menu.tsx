// FILE: src/pages/BayesianPage/menu.tsx

import Button from "../../utilities/button";
import DropDown from "../../utilities/dropdown";
import SelectionBar from "../../utilities/searchbar";
import { TABS } from "../../constants/tabs";

const Menu = ({
  activeLabel,
  setActiveLabel,
  inputValues,
  onInputChange,
  activeLabelAndDropdowns,
  onFileUpload,
  pendingFile,
  onFileSelect
}: any) => {
  const labels = TABS.map(tab => tab.label);
  const labelSeparationPx = 48; // fixed spacing in pixels
  const firstButtonTopPx = 150; // fixed top offset for the first button

  return (
    <>
      {/* --- Left sidebar: fixed search bar on top + fixed buttons --- */}
      <div style={{ position: 'absolute', top: '64px', left: 0, width: '300px', bottom: 0, zIndex: 20 }}>
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
          <SelectionBar
            width="300px"
            height="60px"
            shape="sharp-rectangle"
            x="150px"
            y="30px"
            color="bg-gray-800"
            onFileUpload={onFileUpload}
            pendingFile={pendingFile}
            onFileSelect={onFileSelect}
          />

          {labels.map((label, index) => (
            <Button
              key={label}
              text={label}
              active={activeLabel === label}
              onClick={() => setActiveLabel(label)}
              x={'0'}
              y={`${firstButtonTopPx + index * labelSeparationPx}px`}
              width={'300px'}
              height={'44px'}
              shape={'smooth'}
            />
          ))}
        </div>
      </div>

      {/* --- Main container for the right-side inputs --- */}
      <div
        style={{
          position: 'absolute',
          top: '12.8%',
          left: '300px',
          right: '2%',
          minHeight: '87.2%',
          padding: '2rem',
          minWidth: '300px',
        }}
      >
        {/* --- CONDITIONAL RENDERING: FP Input vs. Dropdowns --- */}
        {activeLabel === 'FP' ? (
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
          // The dropdown grid remains unchanged
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '3rem 1.5rem',
            }}
          >
            {activeLabelAndDropdowns?.children.map((child: any) => {
              const uniqueKey = `${activeLabelAndDropdowns.label}/${child.label}`;
              return (
                <div key={uniqueKey} style={{ position: 'relative', minHeight: '100px' }}>
                  <DropDown
                    label={child.label}
                    label_color="text-gray-800"
                    options={child.values}
                    selectedOption={inputValues[uniqueKey] || child.values[0]}
                    onSelect={(value) => onInputChange(uniqueKey, value)}
                    x="50%"
                    y="50%"
                    width="90%"
                    height="100%"
                    textColor="text-gray-800"
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
}

export default Menu;