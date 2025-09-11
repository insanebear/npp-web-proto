import { css } from "@emotion/react";
// Make sure these paths are correct for your project structure
import { COLORS } from '../../constants/COLORS';
import { FONT_SIZE } from "../../constants/FONT_SIZE";

export const cssObj = {

  pageWrapper: css`
  background-color: ${COLORS.white};
  color: ${COLORS.gray900};
  min-height: 100vh;
  width: 100vw;   /* ensures full width */
  display: flex;
  flex-direction: column;
  padding-top: 80px;
`,


  mainContent: css`
    max-width: 1280px;
    margin: 0 auto;
  `,

  container: css`
    width: 100%;
    margin: 0 auto;
    padding: 0 20px;
  `,

  title: css`
    font-size: ${FONT_SIZE["3xl"]};
    margin-bottom: 2rem;
  `,

  settingsTitleSection: css`
    margin-top: 30px;
  `,

  settingsGrid: css`
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
  `,

  settingBox: css`
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  `,

  longSettingBox: css`
    // If you want long boxes to span more columns in a multi-column layout
    // grid-column: span 2; 
  `,

  inputLabel: css`
    font-weight: 500;
    margin-bottom: 8px;
    color: ${COLORS.gray700};
    font-size: ${FONT_SIZE.sm};
  `,

  inputBox: css`
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid ${COLORS.gray300};
    width: 100%;
    font-size: ${FONT_SIZE.sm};
    background-color: ${COLORS.white};

    &[type='checkbox'] {
      width: auto;
      height: 20px;
      width: 20px;
    }
  `,

  saveButtonContainer: css`
    position: fixed;
    bottom: 30px;
    right: 30px;
  `,

  saveButton: css`
    padding: 10px 24px;
    background-color: ${COLORS.blue600};
    color: ${COLORS.white};
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: ${FONT_SIZE.base};
    font-weight: 500;
    transition: background-color 0.2s;

    &:hover {
      background-color: ${COLORS.blue600};
    }
  `,
};