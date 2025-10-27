// FILE: src/utilities/button.tsx

import React, { type CSSProperties } from 'react';

// ADDED: Props interface
interface ButtonProps {
  text: string;
  active?: boolean;
  onClick: () => void;
  shape?: 'sharp' | 'smooth' | 'circle';
  activeColor?: string;
  hoverColor?: string;
  textColor?: string;
  activeTextColor?: string;
  width?: string | null;
  height?: string | null;
  x?: string;
  y?: string;
  customClasses?: string;
  disabled?: boolean; // ADDED: The missing disabled prop
}

const Button: React.FC<ButtonProps> = ({
  text,
  active = false,
  onClick,
  shape = 'smooth',
  activeColor = 'bg-sky-500',
  hoverColor = 'border-sky-300',
  textColor = 'text-white',
  activeTextColor = 'text-white',
  width = null,
  height = null,
  x = '50%',
  y = '50%',
  customClasses = '',
  disabled = false,
}) => {
  const baseClasses = 'font-semibold focus:outline-none transition-all duration-300 ease-in-out border-2 flex items-center justify-center text-center';
  let shapeClasses = '';
  let paddingClasses = 'px-5 py-2';

  switch (shape) {
    case 'sharp':
      shapeClasses = 'rounded-none';
      break;
    case 'circle':
      shapeClasses = 'rounded-full';
      paddingClasses = '';
      break;
    case 'smooth':
    default:
      shapeClasses = 'rounded-lg';
      break;
  }

  const activeClasses = `${activeColor} ${activeTextColor} border-transparent`;
  const inactiveClasses = `bg-transparent ${textColor} hover:${hoverColor} border-transparent`;

  const finalClassName = `
    ${baseClasses}
    ${shapeClasses}
    ${!width && !height ? paddingClasses : ''}
    ${active ? activeClasses : inactiveClasses}
    ${customClasses}
  `.replace(/\s+/g, ' ').trim();

  // FIXED: Explicitly typed the style object
  const buttonStyle: CSSProperties = {
    position: 'absolute',
    top: y,
    left: x,
    width: width || undefined,
    height: height || undefined,
  };

  if (shape === 'circle') {
    if (width && !height) buttonStyle.height = width;
    if (height && !width) buttonStyle.width = height;
    if (!width && !height) {
      buttonStyle.width = '96px';
      buttonStyle.height = '96px';
    }
  }

  return (
    <button
      onClick={onClick}
      className={finalClassName}
      style={buttonStyle}
      disabled={disabled} // FIXED: Added disabled attribute
    >
      {text}
    </button>
  );
};

export default Button;
