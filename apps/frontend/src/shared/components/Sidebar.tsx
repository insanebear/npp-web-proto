import type { ReactNode } from 'react';

interface SidebarProps {
  children?: ReactNode;
}

const Sidebar = ({ children }: SidebarProps) => {
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
      <div style={{ display: 'flex', flexDirection: 'column', width: '100%', height: '100%' }}>
        {children}
      </div>
    </div>
  );
};

export default Sidebar;
