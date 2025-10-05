// FILE: src/NavigationBar/navItem.tsx

import React, { type CSSProperties } from 'react';
import { Link } from 'react-router-dom';

// ADDED: Props interface and exported it for use in other components
export interface NavItemProps {
  text: string;
  to: string;
  position?: { x: string; y: string };
  size?: string;
  font?: string;
  color?: string;
  activeColor?: string;
  hoverColor?: string;
  active?: boolean;
  onClick?: (text: string) => void; // FIXED: Made onClick optional and typed it
}

const NavItem: React.FC<NavItemProps> = ({
  text,
  to,
  position = { x: '50%', y: '50%' },
  size = 'text-sm',
  font = 'mono',
  color = "text-gray-800",
  activeColor = "text-red-800",
  hoverColor = "hover:text-blue-400",
  active = false,
  onClick,
}) => {
  // FIXED: Explicitly typed the style object
  const itemStyle: CSSProperties = {
    position: 'absolute',
    top: position.y,
    left: position.x,
    transform: 'translate(-50%, -50%)',
  };

  const finalClasses = `
    cursor-pointer transition-colors duration-300 bg-transparent border-none
    p-2 focus:outline-none font-${font} ${size}
    ${active ? `${activeColor} font-bold` : `${color} ${hoverColor}`}
    no-underline
  `;

  return (
    <Link
      to={to}
      style={itemStyle}
      className={finalClasses}
      onClick={() => onClick && onClick(text)}
    >
      {text}
    </Link>
  );
};

export default NavItem;
