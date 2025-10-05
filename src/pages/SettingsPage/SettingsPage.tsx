// FILE: src/pages/SettingsPage/SettingsPage.tsx

/** @jsxImportSource @emotion/react */
import { cssObj } from "./style";
import { useState, type ChangeEvent } from "react";
import type { AppSettings } from "../../hooks/useAppSettings";

// FIXED: Use a partial AppSettings type for the props
type SettingsPageProps = Pick<AppSettings,
  'nChains' | 'nIter' | 'nBurnin' | 'computeDIC' | 'nThin' |
  'setnChains' | 'setnIter' | 'setnBurnin' | 'setcomputeDIC' | 'setnThin'
>;

export default function SettingsPage({
  nChains, nIter, nBurnin, computeDIC, nThin,
  setnChains, setnIter, setnBurnin, setcomputeDIC, setnThin,
}: SettingsPageProps) {

  const [inputValues, setInputValues] = useState({
    UnsavednChains: nChains,
    UnsavednIter: nIter,
    UnsavednBurnin: nBurnin,
    UnsavedcomputeDIC: computeDIC,
    UnsavednThin: nThin,
  });

  // FIXED: Added types for event and key
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>, key: string) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    const valueKey = determineValue(key);
    if (valueKey) {
        setInputValues(prevValues => ({
            ...prevValues,
            [valueKey]: value
        }));
    }
  }

  const handleSave = () => {
    setnChains(Number(inputValues.UnsavednChains));
    setnIter(Number(inputValues.UnsavednIter));
    setnBurnin(Number(inputValues.UnsavednBurnin));
    setcomputeDIC(inputValues.UnsavedcomputeDIC);
    setnThin(Number(inputValues.UnsavednThin));
    alert('Settings Saved!');
  }

  const determineType = (key: string) => {
    if (key.startsWith("N")) { return 'number' }
    else if (key.startsWith('B')) { return 'checkbox' }
    else { return 'text' }
  }

  // FIXED: Added a return type
  const determineValue = (key: string): keyof typeof inputValues | null => {
    if (key === 'N1') return 'UnsavednChains';
    if (key === 'N2') return 'UnsavednIter';
    if (key === 'N3') return 'UnsavednBurnin';
    if (key === 'N4') return 'UnsavednThin';
    if (key === 'B2') return 'UnsavedcomputeDIC';
    return null;
  }

  const settingsFields = [
    { label: "Number of Chains", key: "N1" },
    { label: "Number of Iterations", key: "N2" },
    { label: "Number of Burns", key: "N3" },
    { label: "Thinning Rate", key: "N4" },
    { label: "Compute DIC, pD and deviance", key: "B2" },
  ];

  return (
    <div css={cssObj.pageWrapper}>
      <main css={cssObj.mainContent}>
        <section id="settings-title-section" css={[cssObj.container, cssObj.settingsTitleSection]}>
          <h1 css={cssObj.title}>BBN Hyperparameters</h1>
        </section>
        <section css={cssObj.settingsGrid}>
          {settingsFields.map(({ label, key }) => { // FIXED: removed non-existent 'long' property
            const valueKey = determineValue(key);
            const inputType = determineType(key);
            if (!valueKey) return null;
            return (
              <div key={key} css={cssObj.settingBox}>
                <label htmlFor={key} css={cssObj.inputLabel}>{label}</label>
                <input
                  type={inputType}
                  id={key}
                  value={inputType === 'checkbox' ? undefined : String(inputValues[valueKey])}
                  checked={inputType === 'checkbox' ? Boolean(inputValues[valueKey]) : undefined}
                  onChange={(e) => handleInputChange(e, key)}
                  css={cssObj.inputBox}
                />
              </div>
            );
          })}
        </section>
      </main>
      <div css={cssObj.saveButtonContainer}>
        <button css={cssObj.saveButton} onClick={handleSave}>
          Save
        </button>
      </div>
    </div>
  );
}
