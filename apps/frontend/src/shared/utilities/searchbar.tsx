import React, { useRef, useState, type CSSProperties } from 'react';

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
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    padding: '6px 14px',
    height: '34px',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    fontSize: '13px',
    fontWeight: '600',
    borderRadius: '6px',
    border: 'none',
    cursor: isLoading ? 'not-allowed' : 'pointer',
    whiteSpace: 'nowrap',
    flexShrink: 0,
    transition: 'background-color 0.2s',
    opacity: isLoading ? 0.7 : 1,
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
        onMouseEnter={(e) => { if (!isLoading) e.currentTarget.style.backgroundColor = '#1d4ed8'; }}
        onMouseLeave={(e) => { if (!isLoading) e.currentTarget.style.backgroundColor = '#2563eb'; }}
      >
        <UploadIcon size={14} />
        {isLoading ? 'Loading...' : 'Choose file'}
      </button>
      <span style={fileNameStyle} title={fileName ?? ''}>
        {fileName ?? 'No file chosen'}
      </span>
    </div>
  );
};

export default SelectionBar;
