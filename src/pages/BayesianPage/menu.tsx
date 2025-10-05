// FILE: src/pages/BayesianPage/menu.tsx

import Button from "../../utilities/button";
import DropDown from "../../utilities/dropdown";
import { TABS } from "../../constants/tabs";

const Menu = ({
  activeLabel,
  setActiveLabel,
  dropdownValues,
  handleSelectionChange,
  activeLabelAndDropdowns
}: any) => {
  const labels = TABS.map(tab => tab.label);
  const labelSeparation = 5;

  return (
    <>
      {/* --- Left-side Tab Buttons (No Change) --- */}
      {labels.map((label, index) => (
        <Button
          key={label}
          text={label}
          active={activeLabel === label}
          onClick={() => setActiveLabel(label)}
          x={'2%'}
          y={`${23 + index * labelSeparation}%`}
          width={'20%'}
          height={'5%'}
          shape={'smooth'}
        />
      ))}

      {/* ADDED: A scrollable container for the dropdowns. */}
      {/* This div is positioned to perfectly overlap the gray background area. */}
      <div
        style={{
          position: 'absolute',
          top: '12.8%', // Positioned below the nav and search bars
          left: '25%',   // Starts after the left column
          width: '75%',
          height: '87.2%', // Fills the remaining vertical space
          overflowY: 'auto', // Adds a scrollbar ONLY when needed
          padding: '2rem', // Adds some space around the content
        }}
      >
        {/* UPDATED: Dropdowns are now placed in a CSS Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)', // Arrange in 4 equal columns
            gap: '3rem 1.5rem', // Defines vertical and horizontal spacing
          }}
        >
          {activeLabelAndDropdowns?.children.map((child: any) => {
            const uniqueKey = `${activeLabelAndDropdowns.label}/${child.label}`;
            return (
              // Each dropdown is now a grid item. The wrapper div is necessary
              // for the DropDown's absolute positioning to work within the grid cell.
              <div key={uniqueKey} style={{ position: 'relative', minHeight: '100px' }}>
                <DropDown
                  label={child.label}
                  label_color="text-gray-800"
                  options={child.values}
                  selectedOption={dropdownValues[uniqueKey] || child.values[0]}
                  onSelect={(value) => handleSelectionChange(uniqueKey, value)}
                  // These props now center the dropdown within its grid cell
                  x="50%"
                  y="50%"
                  width="90%" // Use slightly less than 100% width for nice spacing
                  height="100%"
                  textColor="text-gray-800"
                />
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

export default Menu;
