// FILE: src/utilities/rectangle.tsx

import React, { useState, Children, cloneElement, CSSProperties } from 'react';

// ADDED: Props interface
type Shape = 'smooth-rectangle' | 'sharp-rectangle' | 'pill' | 'circle';

interface RectangleProps {
  width?: string;
  height?: string;
  color?: string;
  center?: { x: string; y: string; };
  shape?: Shape;
  children?: React.ReactNode;
  defaultActive?: string;
  onNavigate?: (itemName: string) => void;
}

const Rectangle: React.FC<RectangleProps> = ({
  width = '50%',
  height = '50%',
  color = 'bg-red-100',
  center = { x: '50%', y: '50%' },
  shape = 'sharp-rectangle',
  children,
  defaultActive,
  onNavigate,
}) => {
  const firstChildText = (Children.toArray(children)[0] as React.ReactElement)?.props?.text || '';
  const [activeItem, setActiveItem] = useState(defaultActive || firstChildText);

  // FIXED: Added type for itemName
  const handleItemClick = (itemName: string) => {
    setActiveItem(itemName);
    if (onNavigate) {
      onNavigate(itemName);
    }
  };

  // FIXED: Explicitly typed style object
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
          // FIXED: Used type guard before cloning
          if (React.isValidElement(child)) {
            return cloneElement(child, {
              active: child.props.text === activeItem,
              onClick: handleItemClick,
            });
          }
          return child;
        })}
      </div>
    </div>
  );
};

export default Rectangle;