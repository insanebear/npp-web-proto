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
  textColor = 'text-white',
  activeTextColor = 'text-white',
  width = null,
  height = null,
  x = '50%',
  y = '50%',
  disabled = false,
}) => {
  // Convert Tailwind classes to inline styles
  const getShapeStyles = () => {
    switch (shape) {
      case 'sharp':
        return { borderRadius: '0' };
      case 'circle':
        return { borderRadius: '50%' };
      case 'smooth':
      default:
        return { borderRadius: '8px' };
    }
  };

  const getColorStyles = () => {
    if (active) {
      // Parse activeColor (e.g., 'bg-sky-500' -> '#0ea5e9')
      const bgColor = activeColor === 'bg-sky-500' ? '#0ea5e9' : 
                     activeColor === 'bg-blue-600' ? '#2563eb' : '#0ea5e9';
      const activeTextColorValue = activeTextColor === 'text-white' ? '#ffffff' : '#ffffff';
      return { backgroundColor: bgColor, color: activeTextColorValue, border: 'none' };
    } else {
      // Parse textColor (e.g., 'text-white' -> '#ffffff')
      const textColorValue = textColor === 'text-white' ? '#ffffff' : 
                            textColor === 'text-gray-800' ? '#1f2937' : '#ffffff';
      return { backgroundColor: 'transparent', color: textColorValue, border: 'none' };
    }
  };

  const baseStyles = {
    fontWeight: '600',
    outline: 'none',
    transition: 'all 0.3s ease-in-out',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    textAlign: 'center' as const,
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.6 : 1,
    ...getShapeStyles(),
    ...getColorStyles(),
  };

  const paddingStyles = !width && !height ? { padding: '8px 20px' } : {};

  // FIXED: Explicitly typed the style object
  const buttonStyle: CSSProperties = {
    position: 'absolute',
    top: y,
    left: x,
    width: width || undefined,
    height: height || undefined,
    ...baseStyles,
    ...paddingStyles,
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
      style={buttonStyle}
      disabled={disabled} // FIXED: Added disabled attribute
    >
      {text}
    </button>
  );
};

export default Button;
