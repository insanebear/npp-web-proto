// FILE: src/NavigationBar/navigationBar.tsx

import React, { Children, cloneElement, type CSSProperties, type ReactElement } from 'react';
import { useLocation } from 'react-router-dom';
import type { NavItemProps } from './navItem';

// ADDED: A type definition for the component's props
type Shape = 'smooth-rectangle' | 'sharp-rectangle' | 'pill' | 'circle';

interface NavigationBarProps {
  width?: string;
  height?: string;
  color?: string;
  center?: { x: string; y: string };
  shape?: Shape;
  children: React.ReactNode;
  onNavigate?: (itemName: string) => void;
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
  } else if (location.pathname === '/' || location.pathname.startsWith('/bayesian')) {
    activeItemText = "Bayesian Methods";
  }

  const handleItemClick = (itemName: string) => {
    if (onNavigate) {
      onNavigate(itemName);
    }
  };

  const barStyle: CSSProperties = {
    position: 'absolute',
    '--bar-width': width,
    '--bar-height': height,
    width: 'var(--bar-width)',
    height: 'var(--bar-height)',
    top: `clamp(calc(var(--bar-height) / 2), ${center.y}, calc(100% - var(--bar-height) / 2))`,
    left: `clamp(calc(var(--bar-width) / 2), ${center.x}, calc(100% - var(--bar-width) / 2))`,
    transform: 'translate(-50%, -50%)',
  } as CSSProperties;

  const shapeClasses: { [key in Shape]: string } = {
    'smooth-rectangle': 'rounded-lg',
    'sharp-rectangle': 'rounded-none',
    'pill': 'rounded-full',
    'circle': 'rounded-full',
  };
  const shapeClass = shapeClasses[shape] || shapeClasses['smooth-rectangle'];

  return (
    <div style={barStyle} className={`${color} ${shapeClass} shadow-lg transition-all duration-300`}>
      <div className="flex justify-between items-center w-full h-full px-4">
        {Children.map(children, (child, index) => {
          if (React.isValidElement(child)) {
            const typedChild = child as ReactElement<NavItemProps>;
            return cloneElement(typedChild, {
              ...typedChild.props,
              active: typedChild.props.text === activeItemText,
              onClick: handleItemClick,
              className: `${typedChild.props.className || ''} ${index === 3 ? 'ml-auto' : ''}`,
            });
          }
          return child;
        })}
      </div>
    </div>
  );
};

export default NavigationBar;