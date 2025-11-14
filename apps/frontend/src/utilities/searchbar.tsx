// FILE: src/utilities/searchbar.tsx

import React, { useRef, type CSSProperties } from 'react';

const SearchIcon = ({ size }: { size: number }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" viewBox="0 0 16 16">
    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
  </svg>
);

const UploadIcon = ({ size }: { size: number }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" viewBox="0 0 16 16">
    <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" />
    <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z" />
  </svg>
);

interface SelectionBarProps {
  width?: string;
  height?: string;
  shape?: 'smooth-rectangle' | 'sharp-rectangle';
  x?: string;
  y?: string;
  color?: string;
  onFileUpload?: (fileContent: string) => void;
  pendingFile: File | null;
  onFileSelect: (file: File) => void;
}

const SelectionBar: React.FC<SelectionBarProps> = ({
  width = 'calc(100% - 2rem)',
  height = '60px',
  shape = 'smooth-rectangle',
  y = '50%',
  color = 'bg-gray-800',
  onFileUpload,
  pendingFile,
  onFileSelect,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const selectionName = pendingFile ? pendingFile.name : 'Select a file';

  const handleSearchClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
    // ✨ FIX: Reset the input's value after handling the file.
    // This allows the onChange event to fire even if the same file is selected again.
    event.target.value = '';
  };

  const handleUploadClick = () => {
    if (pendingFile && onFileUpload) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        if (text) {
          onFileUpload(text);
        }
      };
      reader.readAsText(pendingFile);
    } else {
      alert('Please select a file using the "Search" button first.');
    }
  };
 
  const baseFontSize = 14, baseIconSize = 18, baseButtonHeight = 44, baseButtonPaddingX = 18, baseGap = 10, baseContainerPadding = 10;
  const fontSize = baseFontSize, iconSize = baseIconSize, buttonHeight = baseButtonHeight, buttonPaddingX = baseButtonPaddingX, gap = baseGap, containerPadding = baseContainerPadding;
  
  const containerStyle: CSSProperties = { 
    position: 'absolute', 
    top: y,
    width: width, 
    height: height, 
    transform: 'translateY(-50%)', 
    padding: `${containerPadding}px`, 
    gap: `${gap}px`,
    minWidth: '300px',
    maxWidth: 'calc(100% - 2rem)'
  };
  const selectionTextStyle = { fontSize: `${fontSize}px` };
  const buttonStyle = { height: `${buttonHeight}px`, paddingLeft: `${buttonPaddingX}px`, paddingRight: `${buttonPaddingX}px`, fontSize: `${fontSize}px`, borderRadius: '8px' };
  const shapeClass = shape === 'smooth-rectangle' ? 'rounded-xl' : 'rounded-none';

  // Convert Tailwind classes to inline styles
  const getBackgroundColor = () => {
    return color === 'bg-gray-800' ? '#1f2937' : '#f3f4f6';
  };

  const getBorderRadius = () => {
    return shapeClass === 'rounded-xl' ? '12px' : '0';
  };

  const containerStyleWithClasses: CSSProperties = {
    ...containerStyle,
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: getBackgroundColor(),
    borderRadius: getBorderRadius(),
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  };

  const inputStyle: CSSProperties = {
    display: 'none',
  };

  const textContainerStyle: CSSProperties = {
    width: '100%',
    padding: '8px 16px',
  };

  const textStyle: CSSProperties = {
    ...selectionTextStyle,
    color: '#d1d5db',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  };

  const buttonContainerStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    padding: '0 16px 8px 16px',
    gap: `${gap}px`,
    marginTop: '4px',
  };

  const searchButtonStyle: CSSProperties = {
    ...buttonStyle,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(55, 65, 81, 0.5)',
    color: '#ffffff',
    fontWeight: '600',
    transition: 'all 0.2s',
    outline: 'none',
    whiteSpace: 'nowrap',
  };

  const uploadButtonStyle: CSSProperties = {
    ...buttonStyle,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    fontWeight: '600',
    transition: 'all 0.2s',
    outline: 'none',
    whiteSpace: 'nowrap',
  };

  return (
    <div style={containerStyleWithClasses}>
      <input
        type="file"
        accept=".json"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={inputStyle}
      />
      <div style={textContainerStyle}>
        <p style={textStyle} title={selectionName}>
          {selectionName}
        </p>
      </div>
      <div style={buttonContainerStyle}>
        <button
          onClick={handleSearchClick}
          style={searchButtonStyle}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(75, 85, 99, 0.8)'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'rgba(55, 65, 81, 0.5)'}
        >
          <SearchIcon size={iconSize} />
          <span style={{ marginLeft: `${gap}px` }}>Search</span>
        </button>
        <button
          onClick={handleUploadClick}
          style={uploadButtonStyle}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#1d4ed8'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#2563eb'}
        >
          <UploadIcon size={iconSize} />
          <span style={{ marginLeft: `${gap}px` }}>Upload</span>
        </button>
      </div>
    </div>
  );
};

export default SelectionBar;
