// FILE: src/pages/BayesianPage/BayesianPage.tsx

import { useState } from 'react';
import Background from './background';
import Menu from './menu';
import { TABS } from '../../constants/tabs';
import SelectionBar from '../../utilities/searchbar';
import SubmitButton from './bayesian_submit_button/submitButton';

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

  const handleSubmit = () => {
    // The `inputValues` from props now contains FP and all dropdowns.
    const payload = formatPayload(inputValues, settings);
    onStartSimulation(payload);
  };

  const activeLabelAndDropdowns = TABS.find(tab => tab.label === activeLabel);

  return (
    <>
      <Background />
      {jobError && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 p-4 bg-red-100 text-red-800 rounded-md">
          Error: {jobError}
        </div>
      )}
      <SelectionBar
        width="300px" height="6.4%" shape="sharp-rectangle" x="150px" y="9.6%" color="bg-gray-800" scale={0.7}
        onFileUpload={onFileUpload}
        pendingFile={pendingFile}
        onFileSelect={onFileSelect}
      />
      <Menu
        activeLabel={activeLabel}
        setActiveLabel={setActiveLabel}
        inputValues={inputValues} // Pass unified state down
        onInputChange={onInputChange} // Pass unified handler down
        activeLabelAndDropdowns={activeLabelAndDropdowns}
      />
      <SubmitButton
        onClick={handleSubmit}
        status={jobStatus}
        x="87%" y="90%" width="8%" height="5%"
      />
    </>
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