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
  height = '64px',
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
    zIndex: 1000,
  } as CSSProperties;

  // Removed unused shapeClasses

  // Convert Tailwind classes to inline styles
  const getBackgroundColor = () => {
    return color === 'bg-gray-100' ? '#f3f4f6' : 
           color === 'bg-gray-800' ? '#1f2937' : '#f3f4f6';
  };

  const getBorderRadius = () => {
    return shape === 'smooth-rectangle' ? '8px' :
           shape === 'sharp-rectangle' ? '0' :
           shape === 'pill' ? '9999px' : '0';
  };

  const barContainerStyle: CSSProperties = {
    ...barStyle,
    backgroundColor: getBackgroundColor(),
    borderRadius: getBorderRadius(),
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    transition: 'all 0.3s',
  };

  const flexContainerStyle: CSSProperties = {
    display: 'flex',
    justifyContent: 'flex-start',
    alignItems: 'center',
    width: '100%',
    height: '100%',
    padding: '0 16px',
    gap: '32px',
  };

  // Ensure last item (Settings) sticks to the right edge
  const items = Children.toArray(children);

  return (
    <div style={barContainerStyle}>
      <div style={flexContainerStyle}>
        {items.map((child, index) => {
          if (React.isValidElement(child)) {
            const typedChild = child as ReactElement<NavItemProps>;
            const cloned = cloneElement(typedChild, {
              ...typedChild.props,
              active: typedChild.props.text === activeItemText,
              onClick: handleItemClick,
            });

            if (index === items.length - 1) {
              return <div key={`nav-${index}`} style={{ marginLeft: 'auto' }}>{cloned}</div>;
            }
            return <div key={`nav-${index}`}>{cloned}</div>;
          }
          return child as any;
        })}
      </div>
    </div>
  );
};

export default NavigationBar;