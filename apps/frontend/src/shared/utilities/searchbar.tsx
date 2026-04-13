import React, { useRef, useState, type CSSProperties } from 'react';


interface SelectionBarProps {
  width?: string;
  height?: string;
  shape?: 'smooth-rectangle' | 'sharp-rectangle';
  x?: string;
  y?: string;
  color?: string;
  onFileUpload?: (fileContent: string) => void;
  // kept for backward compat but no longer used internally
  pendingFile?: File | null;
  onFileSelect?: (file: File) => void;
}

const SelectionBar: React.FC<SelectionBarProps> = ({
  width = 'calc(100% - 2rem)',
  shape = 'smooth-rectangle',
  y = '50%',
  color = 'bg-gray-800',
  onFileUpload,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChooseClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setIsLoading(true);

    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      if (text && onFileUpload) {
        onFileUpload(text);
      }
      setIsLoading(false);
    };
    reader.onerror = () => setIsLoading(false);
    reader.readAsText(file);

    event.target.value = '';
  };

  const getBackgroundColor = () => color === 'bg-gray-800' ? '#1f2937' : '#f3f4f6';
  const getBorderRadius = () => shape === 'smooth-rectangle' ? '12px' : '0';

  const containerStyle: CSSProperties = {
    position: 'absolute',
    top: y,
    width: width,
    height: 'auto',
    transform: 'translateY(-50%)',
    minWidth: '200px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '8px 12px',
    backgroundColor: getBackgroundColor(),
    borderRadius: getBorderRadius(),
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  };

  const chooseButtonStyle: CSSProperties = {
    padding: '5px 12px',
    fontSize: '14px',
    fontWeight: '500',
    border: '1px solid #D1D5DB',
    borderRadius: '6px',
    backgroundColor: '#FFF',
    color: '#374151',
    cursor: isLoading ? 'not-allowed' : 'pointer',
    whiteSpace: 'nowrap',
    flexShrink: 0,
    transition: 'background-color 0.15s, border-color 0.15s',
    opacity: isLoading ? 0.6 : 1,
  };

  const fileNameStyle: CSSProperties = {
    color: fileName ? '#d1d5db' : '#9ca3af',
    fontSize: '13px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    flex: 1,
  };

  return (
    <div style={containerStyle}>
      <input
        type="file"
        accept=".json"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        disabled={isLoading}
      />
      <button
        style={chooseButtonStyle}
        onClick={handleChooseClick}
        disabled={isLoading}
        onMouseEnter={(e) => { if (!isLoading) { e.currentTarget.style.backgroundColor = '#F3F4F6'; e.currentTarget.style.borderColor = '#9CA3AF'; } }}
        onMouseLeave={(e) => { if (!isLoading) { e.currentTarget.style.backgroundColor = '#FFF'; e.currentTarget.style.borderColor = '#D1D5DB'; } }}
      >
        {isLoading ? 'Loading...' : 'Choose file'}
      </button>
      <span style={fileNameStyle} title={fileName ?? ''}>
        {fileName ?? 'No file chosen'}
      </span>
    </div>
  );
};

export default SelectionBar;
