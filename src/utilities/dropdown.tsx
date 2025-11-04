// FILE: src/utilities/dropdown.tsx

import React, { useState, useEffect, useRef, type CSSProperties } from 'react';
import Button from './button';

// ADDED: Props interface
interface DropDownProps {
  options: readonly string[] | string[];
  selectedOption: string;
  onSelect: (option: string) => void;
  x: string;
  y: string;
  width: string;
  height: string;
  textColor?: string;
  label?: string;
  label_color?: string;
  alignment?: 'left' | 'right' | 'center';
}

const DropDown: React.FC<DropDownProps> = ({
  options,
  selectedOption,
  onSelect,
  x,
  y,
  width,
  height,
  textColor = 'text-white',
  label,
  label_color = 'text-gray-700',
  alignment = 'center',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  // FIXED: Provide the correct element type for the ref
  const dropdownRef = useRef<HTMLDivElement>(null);

  const justifyContentClass = {
    left: 'justify-start',
    right: 'justify-end',
    center: 'justify-center',
  }[alignment];

  useEffect(() => {
    // FIXED: Type the event parameter
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownRef]);

  // FIXED: Type the option parameter
  const handleSelect = (option: string) => {
    onSelect(option);
    setIsOpen(false);
  };

  // FIXED: Explicitly typed the style object
  const containerStyle: CSSProperties = {
    position: 'absolute',
    top: y,
    left: x,
    width: width,
    transform: 'translate(-50%, -50%)',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  };

  return (
    <div style={containerStyle} ref={dropdownRef}>
      {label && (
        <label style={{
          display: 'block',
          fontSize: '14px',
          fontWeight: '500',
          color: label_color === 'text-gray-800' ? '#1f2937' : 
                 label_color === 'text-gray-700' ? '#374151' : '#1f2937',
          textAlign: alignment === 'left' ? 'left' : alignment === 'right' ? 'right' : 'center'
        }}>
          {label}
        </label>
      )}

      <div style={{ 
        position: 'relative', 
        width: '100%', 
        height: height
      }}
      >
        <Button
          text={selectedOption}
          onClick={() => setIsOpen(prev => !prev)}
          x="0"
          y="0"
          width="100%"
          height="100%"
          customClasses={`px-4 ${justifyContentClass}`}
          active={isOpen}
          textColor={textColor}
        />

        {isOpen && (
          <div 
            style={{ 
              position: 'absolute',
              width: '100%',
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
              zIndex: 1000,
              top: '100%',
              marginTop: '20px'
            }}
          >
            {options.map(option => (
              <div
                key={option}
                onClick={() => handleSelect(option)}
                style={{ 
                  height: height, 
                  display: 'flex', 
                  alignItems: 'center',
                  padding: '0 16px',
                  color: '#374151',
                  cursor: 'pointer',
                  transition: 'background-color 0.15s',
                  textAlign: alignment === 'left' ? 'left' : alignment === 'right' ? 'right' : 'center'
                }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f0f9ff'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
              >
                {option}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DropDown;
