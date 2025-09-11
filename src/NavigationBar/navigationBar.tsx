// FILE: src/NavigationBar/navigationBar.tsx

import React, { Children, cloneElement, CSSProperties } from 'react';
import { useLocation } from 'react-router-dom';

// ADDED: A type definition for the component's props
type Shape = 'smooth-rectangle' | 'sharp-rectangle' | 'pill' | 'circle';

interface NavigationBarProps {
  width?: string;
  height?: string;
  color?: string;
  center?: { x: string; y: string };
  shape?: Shape;
  children: React.ReactNode;
  onNavigate?: (itemName: string) => void; // FIXED: Made onNavigate optional
}

const NavigationBar: React.FC<NavigationBarProps> = ({
  width = '100%',
  height = '6.4%',
  color = 'bg-gray-100',
  center = { x: '50%', y: '0%' },
  shape = 'sharp-rectangle',
  children,
  onNavigate,
}) => {
  const location = useLocation();
  let activeItemText = "Bayesian Methods";
  if (location.pathname.startsWith('/reliability-views')) {
    activeItemText = "Reliability Views";
  } else if (location.pathname.startsWith('/statistical')) {
    activeItemText = "Statistical Methods";
  } else if (location.pathname.startsWith('/settings')) {
    activeItemText = "Settings";
  }

  // FIXED: Added type for itemName
  const handleItemClick = (itemName: string) => {
    if (onNavigate) {
      onNavigate(itemName);
    }
  };

  // FIXED: Explicitly typed the style object as React.CSSProperties
  const barStyle: CSSProperties = {
    position: 'absolute',
    '--bar-width': width,
    '--bar-height': height,
    width: 'var(--bar-width)',
    height: 'var(--bar-height)',
    top: `clamp(calc(var(--bar-height) / 2), ${center.y}, calc(100% - var(--bar-height) / 2))`,
    left: `clamp(calc(var(--bar-width) / 2), ${center.x}, calc(100% - var(--bar-width) / 2))`,
    transform: 'translate(-50%, -50%)',
  };

  const shapeClasses: { [key in Shape]: string } = {
    'smooth-rectangle': 'rounded-lg',
    'sharp-rectangle': 'rounded-none',
    'pill': 'rounded-full',
    'circle': 'rounded-full',
  };
  const shapeClass = shapeClasses[shape] || shapeClasses['smooth-rectangle'];

  return (
    <div style={barStyle} className={`${color} ${shapeClass} shadow-lg transition-all duration-300`}>
      <div className="relative w-full h-full">
        {Children.map(children, (child) => {
          // FIXED: Use React.isValidElement as a type guard
          if (React.isValidElement(child)) {
            return cloneElement(child, {
              active: child.props.text === activeItemText,
              onClick: handleItemClick,
            });
          }
          return child;
        })}
      </div>
    </div>
  );
};

export default NavigationBar;