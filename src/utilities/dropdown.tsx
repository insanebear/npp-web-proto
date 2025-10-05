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

  const textAlignClass = {
    left: 'text-left',
    right: 'text-right',
    center: 'text-center',
  }[alignment];

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
        <label className={`block text-sm font-medium ${label_color} ${textAlignClass}`}>
          {label}
        </label>
      )}

      <div className="relative" style={{ width: '100%', height: height }}>
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
          <div className="absolute top-full mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-xl z-10">
            {options.map(option => (
              <div
                key={option}
                onClick={() => handleSelect(option)}
                style={{ height: height, display: 'flex', alignItems: 'center' }}
                className={`px-4 text-gray-700 hover:bg-sky-100 cursor-pointer transition-colors duration-150 ${textAlignClass}`}
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
