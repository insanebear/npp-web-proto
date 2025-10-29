// FILE: src/utilities/rectangle.tsx

import React, { useState, Children, cloneElement, type CSSProperties, type ReactElement } from 'react';

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

// Interface for children that this component will modify.
interface ChildWithClonedProps {
  text: string;
  active?: boolean;
  onClick?: (itemName: string) => void;
  [key: string]: any;
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
  const firstChildText = (Children.toArray(children)[0] as ReactElement<ChildWithClonedProps>)?.props?.text || '';
  const [activeItem, setActiveItem] = useState(defaultActive || firstChildText);

  const handleItemClick = (itemName: string) => {
    setActiveItem(itemName);
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

  // Convert Tailwind classes to inline styles
  const getBackgroundColor = () => {
    return color === 'bg-red-100' ? '#fee2e2' : 
           color === 'bg-gray-800' ? '#1f2937' : '#f3f4f6';
  };

  const getBorderRadius = () => {
    return shapeClass === 'rounded-lg' ? '8px' :
           shapeClass === 'rounded-none' ? '0' :
           shapeClass === 'rounded-full' ? '9999px' : '8px';
  };

  const containerStyle: CSSProperties = {
    ...barStyle,
    backgroundColor: getBackgroundColor(),
    borderRadius: getBorderRadius(),
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    transition: 'all 0.3s',
  };

  const innerContainerStyle: CSSProperties = {
    position: 'relative',
    width: '100%',
    height: '100%',
  };

  return (
    <div style={containerStyle}>
      <div style={innerContainerStyle}>
        {Children.map(children, (child) => {
          if (React.isValidElement(child)) {
            // ======================== FINAL FIX IS HERE ========================
            // Assert the type of the 'child' element itself before cloning.
            const typedChild = child as ReactElement<ChildWithClonedProps>;
            return cloneElement(typedChild, {
              ...typedChild.props,
              active: typedChild.props.text === activeItem,
              onClick: handleItemClick,
            });
            // ====================================================================
          }
          return child;
        })}
      </div>
    </div>
  );
};

export default Rectangle;