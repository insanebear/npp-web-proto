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
  dropdownValues,
  onDropdownChange
}: any) {
  // The active tab state can remain local as it doesn't need to persist across pages.
  const [activeLabel, setActiveLabel] = useState('Requirement Dev');

  // The local state for dropdown values and its related logic have been removed.

  const handleSubmit = () => {
    // The `dropdownValues` are now directly from props.
    const payload = formatPayload(dropdownValues, settings);
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
        width="25%" height="6.4%" shape="sharp-rectangle" x="12.5%" y="9.6%" color="bg-gray-800" scale={0.7}
        onFileUpload={onFileUpload}
        pendingFile={pendingFile}
        onFileSelect={onFileSelect}
      />
      <Menu
        activeLabel={activeLabel}
        setActiveLabel={setActiveLabel}
        dropdownValues={dropdownValues} // Pass prop down
        handleSelectionChange={onDropdownChange} // Pass the handler function from App.tsx
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

const formatPayload = (values: { [key: string]: string }, settings: any) => {
  const payload: { [key: string]: any } = {};
  for (const key in values) {
    const [tabLabel, childLabel] = key.split('/');
    if (!payload[tabLabel]) {
      payload[tabLabel] = {};
    }
    payload[tabLabel][childLabel] = values[key];
  }
  payload['FP'] = { 'FP Input': '120' }; // This is still hardcoded
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
