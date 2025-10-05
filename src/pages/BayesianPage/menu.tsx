// FILE: src/pages/BayesianPage/menu.tsx

import Button from "../../utilities/button";
import DropDown from "../../utilities/dropdown";
import { TABS } from "../../constants/tabs";

const Menu = ({
  activeLabel,
  setActiveLabel,
  inputValues,
  onInputChange,
  activeLabelAndDropdowns
}: any) => {
  const labels = TABS.map(tab => tab.label);
  const labelSeparation = 5;

  return (
    <>
      {/* --- Left-side Tab Buttons --- */}
      {labels.map((label, index) => (
        <Button
          key={label}
          text={label}
          active={activeLabel === label}
          onClick={() => setActiveLabel(label)}
          x={'2%'}
          y={`${23 + index * labelSeparation}%`}
          width={'20%'}
          height={'5%'}
          shape={'smooth'}
        />
      ))}

      {/* --- Main container for the right-side inputs --- */}
      <div
        style={{
          position: 'absolute',
          top: '12.8%',
          left: '25%',
          width: '75%',
          height: '87.2%',
          overflowY: 'auto',
          padding: '2rem',
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
                        width: '250px',
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
              gridTemplateColumns: 'repeat(4, 1fr)',
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