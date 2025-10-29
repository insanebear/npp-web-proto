// FILE: src/NavigationBar/navItem.tsx

import React, { type CSSProperties } from 'react';
import { Link } from 'react-router-dom';

// ADDED: Props interface and exported it for use in other components
export interface NavItemProps {
  text: string;
  to: string;
  size?: string;
  font?: string;
  color?: string;
  activeColor?: string;
  hoverColor?: string;
  active?: boolean;
  onClick?: (text: string) => void; // FIXED: Made onClick optional and typed it
  className?: string;
}

const NavItem: React.FC<NavItemProps> = ({
  text,
  to,
  size = 'text-base',
  font = 'sans',
  color = "text-gray-800",
  activeColor = "text-red-800",
  active = false,
  onClick,
}) => {
  // FIXED: Explicitly typed the style object
  const itemStyle: CSSProperties = {
    // Remove absolute positioning to work with flexbox
  };

  // Convert Tailwind classes to inline styles
  const getTextColor = () => {
    if (active) {
      return activeColor === 'text-red-800' ? '#991b1b' : '#dc2626';
    } else {
      return color === 'text-gray-800' ? '#1f2937' : '#374151';
    }
  };

  const getFontSize = () => {
    return size === 'text-base' ? '16px' : 
           size === 'text-sm' ? '14px' : 
           size === 'text-lg' ? '18px' : '16px';
  };

  const getFontFamily = () => {
    return font === 'mono' ? 'monospace' : 
           font === 'sans' ? 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' : 
           'system-ui, sans-serif';
  };

  const linkStyle: CSSProperties = {
    cursor: 'pointer',
    transition: 'color 0.3s',
    backgroundColor: 'transparent',
    border: 'none',
    padding: '8px',
    outline: 'none',
    fontFamily: getFontFamily(),
    fontSize: getFontSize(),
    color: getTextColor(),
    fontWeight: 'bold',
    textDecoration: 'none',
    ...itemStyle,
  };

  return (
    <Link
      to={to}
      style={linkStyle}
      onClick={() => onClick && onClick(text)}
    >
      {text}
    </Link>
  );
};

export default NavItem;
