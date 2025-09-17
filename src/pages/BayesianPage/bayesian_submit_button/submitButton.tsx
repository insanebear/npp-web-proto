// FILE: C:\Users\lab\Desktop\npp-web-proto\src\pages\BayesianPage\bayesian_submit_button\submitButton.tsx

import React from 'react';
import Button from '../../../utilities/button';

interface SubmitButtonProps {
  onClick: () => void;
  status: string | null;
  x?: string;
  y?: string;
  width?: string;
  height?: string;
}

const SubmitButton: React.FC<SubmitButtonProps> = ({
  onClick,
  status,
  ...buttonProps
}) => {
  // A simulation is "busy" if it has a status that is not final (COMPLETED/FAILED) or null.
  const isBusy = status !== null && status !== 'COMPLETED' && status !== 'FAILED';

  const getButtonText = (): string => {
    if (!isBusy || !status) {
      return 'Submit';
    }
    // Capitalize first letter and add ellipsis for a consistent look (e.g., "Running...").
    return `${status.charAt(0).toUpperCase() + status.slice(1).toLowerCase()}...`;
  };

  return (
    <Button
      text={getButtonText()}
      onClick={onClick}
      disabled={isBusy}
      active={true}
      // The button is grayed out and non-interactive when busy.
      activeColor={isBusy ? 'bg-gray-500' : 'bg-red-700'}
      customClasses="hover:bg-blue-600 active:bg-green-500 text-white"
      shape="smooth"
      {...buttonProps}
    />
  );
};

export default SubmitButton;