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

  return (
    <div
      style={containerStyle}
      className={`flex flex-col ${color} ${shapeClass} shadow-2xl border border-white/10`}
    >
      <input
        type="file"
        accept=".json"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
      <div className="w-full px-4 py-2">
        <p className="text-gray-300 truncate" style={selectionTextStyle} title={selectionName}>
          {selectionName}
        </p>
      </div>
      <div className="flex items-center justify-center w-full px-4 pb-2" style={{ gap: `${gap}px`, marginTop: '4px' }}>
        <button
          onClick={handleSearchClick}
          style={buttonStyle}
          className="flex items-center justify-center bg-gray-700/50 hover:bg-gray-600/80 text-white font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white whitespace-nowrap"
        >
          <SearchIcon size={iconSize} />
          <span style={{ marginLeft: `${gap}px` }}>Search</span>
        </button>
        <button
          onClick={handleUploadClick}
          style={buttonStyle}
          className="flex items-center justify-center bg-blue-600 hover:bg-blue-500 text-white font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white whitespace-nowrap"
        >
          <UploadIcon size={iconSize} />
          <span style={{ marginLeft: `${gap}px` }}>Upload</span>
        </button>
      </div>
    </div>
  );
};

export default SelectionBar;
