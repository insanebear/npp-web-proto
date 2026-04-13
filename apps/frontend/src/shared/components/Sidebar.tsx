import type { ReactNode } from 'react';
import SelectionBar from '../utilities/searchbar';

interface SidebarProps {
  onFileUpload?: (fileContent: string) => void;
  pendingFile?: File | null;
  onFileSelect?: (file: File) => void;
  children?: ReactNode;
}

const Sidebar = ({ onFileUpload, pendingFile, onFileSelect, children }: SidebarProps) => {
  return (
    <div style={{
      position: 'absolute',
      top: '64px',
      left: 0,
      width: '300px',
      bottom: 0,
      backgroundColor: '#ffffff',
      borderRight: '1px solid #E5E7EB',
      zIndex: 20,
    }}>
      <div style={{ position: 'relative', width: '100%', height: '100%' }}>
        <SelectionBar
          width="300px"
          height="60px"
          shape="sharp-rectangle"
          x="150px"
          y="30px"
          color="bg-white"
          onFileUpload={onFileUpload}
          pendingFile={pendingFile}
          onFileSelect={onFileSelect}
        />
        {children}
      </div>
    </div>
  );
};

export default Sidebar;
