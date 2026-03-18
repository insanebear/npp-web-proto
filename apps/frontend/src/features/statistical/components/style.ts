import { COLORS } from '../../../shared/constants/COLORS'
import { FONT_SIZE } from "../../../shared/constants/FONT_SIZE";
import { css } from "@emotion/react";

export const cssObj = {
  globalStyles: css`
    body {
      margin: 0;
      background-color: #E5E7EB
    }
  `,

  pageWrapper: css`
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #E5E7EB
  `,
  header: css`
    background-color: ${COLORS.gray800};
    height: 60px;
    flex-shrink: 0;
    & > div {
      display: flex;
      align-items: center;
      height: 100%;
      justify-content: space-between;
    }
    & > div > div {
      display: flex;
      align-items: center;
    }
    & > div img {
      margin-right: 20px;
    }
    & button {
      background: transparent;
      border: none;
      color: ${COLORS.gray300};
      font-size: ${FONT_SIZE.xs};
      height: 60px;
      margin-left: 20px;
      margin-right: 0;
      cursor: pointer;
      transition: color 0.2s;
      &:hover {
        color: ${COLORS.white};
      }
    }
    & button.active,
    & button:focus {
      color: ${COLORS.white};
      outline: none;
    }
  `,
  active: css`
    color: ${COLORS.white} !important;
  `,
  container: css`
    width: 90%;
    max-width: 1600px;
    box-sizing: border-box;
  `,
  mainContent: css`
    flex-grow: 1;
    padding-bottom: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
  `,
  settingsTitleSection: css`
    margin-top: 80px;
    margin-bottom: 24px;
  `,
  bbnSelectorBox: css`
    width: 90%;
    max-width: 1200px;
    background-color: ${COLORS.white};
    border: 1px solid ${COLORS.gray200};
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    margin-bottom: 16px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 12px;
  `,
  bbnSelectorHeader: css`
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    h2 {
      font-size: ${FONT_SIZE.base};
      font-weight: 600;
      color: ${COLORS.gray800};
      margin: 0;
    }
    p {
      margin: 4px 0 0;
      font-size: ${FONT_SIZE.xs};
      color: ${COLORS.gray500};
    }
  `,
  bbnSelect: css`
    width: 100%;
    padding: 10px 12px;
    border-radius: 6px;
    border: 1px solid ${COLORS.gray300};
    background-color: ${COLORS.white};
    font-size: ${FONT_SIZE.sm};
    color: ${COLORS.gray800};
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s;
    &:focus {
      outline: none;
      border-color: ${COLORS.blue600};
      box-shadow: 0 0 0 1px ${COLORS.blue600};
    }
  `,
  bbnMetaInfo: css`
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    font-size: ${FONT_SIZE.xs};
    color: ${COLORS.gray600};
  `,
  bbnActionRow: css`
    display: flex;
    align-items: center;
    gap: 12px;
  `,
  bbnButton: css`
    padding: 6px 12px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    font-size: ${FONT_SIZE.sm};
    font-weight: 500;
    transition: background-color 0.2s;
  `,
  bbnPrimaryButton: css`
    background-color: ${COLORS.blue600};
    color: ${COLORS.white};
    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  `,
  bbnSecondaryButton: css`
    background-color: ${COLORS.green600};
    color: ${COLORS.white};
    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  `,
  bbnRefreshButton: css`
    padding: 6px 12px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    font-size: ${FONT_SIZE.sm};
    font-weight: 500;
    background-color: ${COLORS.gray700};
    color: ${COLORS.white};
    transition: background-color 0.2s;
    &:hover {
      background-color: ${COLORS.gray600};
    }
    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  `,
  bbnMessage: css`
    font-size: ${FONT_SIZE.xs};
    color: ${COLORS.gray600};
  `,
  bbnErrorText: css`
    font-size: ${FONT_SIZE.xs};
    color: #dc2626;
  `,
  title: css`
    font-size: ${FONT_SIZE["3xl"]};
    color: ${COLORS.gray800};
    font-weight: 700;
  `,
  rightSection: css`
    display: flex;
    align-items: center;
    gap: 20px;
  `,
  newButton: css`
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    background-color: ${COLORS.gray700};
    color: ${COLORS.white};
    border: none;
    font-size: ${FONT_SIZE.sm};
    &:hover {
      background-color: ${COLORS.gray600};
    }
  `,
  settingsGrid: css`
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    column-gap: 20px;
    row-gap: 24px;
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
  `,
  settingBox: css`
    background-color: ${COLORS.white};
    border: 1px solid ${COLORS.gray200};
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    gap: 16px;
    h2 {
      font-size: ${FONT_SIZE.base};
      font-weight: 600;
      color: ${COLORS.gray800};
      margin: 0;
    }
  `,
  formWrapper: css`
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 16px;
  `,
  inputGroup: css`
    display: flex;
    flex-direction: column;
    gap: 6px;
  `,
  inputLabel: css`
    font-size: ${FONT_SIZE.sm};
    font-weight: 500;
    color: ${COLORS.gray700};
  `,
  inputBox: css`
    padding: 10px 12px;
    border-radius: 6px;
    border: 1px solid ${COLORS.gray300};
    font-size: ${FONT_SIZE.sm};
    color: ${COLORS.gray800};
    background-color: ${COLORS.white};
    width: 100%;
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s;
    &:focus {
      outline: none;
      border-color: ${COLORS.blue600};
      box-shadow: 0 0 0 1px ${COLORS.blue600};
    }
  `,
  saveButton: css`
    padding: 10px 16px;
    background-color: ${COLORS.blue600};
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: ${FONT_SIZE.sm};
    font-weight: 600;
    align-self: flex-start;
    transition: background-color 0.2s;
    &:hover:not(:disabled) {
      background-color: #1d4ed8;
    }
    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  `,
  output: css`
    margin-top: 16px;
    padding: 12px;
    background-color: ${COLORS.gray50};
    border-radius: 6px;
    font-size: ${FONT_SIZE.sm};
    color: ${COLORS.gray700};
    p {
      margin: 0;
    }
    p + p {
      margin-top: 8px;
    }
    a {
      color: ${COLORS.blue600};
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }
  `,

  // ── Sensitivity Analysis: Required # of tests output box ──
  outputBox: css`
    background-color: ${COLORS.gray50};
    border: 1px solid ${COLORS.gray200};
    border-radius: 6px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-top: 4px;
  `,
  outputLabel: css`
    font-size: ${FONT_SIZE.xs};
    color: ${COLORS.gray500};
    font-weight: 500;
  `,
  outputValue: css`
    font-size: ${FONT_SIZE.base};
    font-weight: 600;
    color: ${COLORS.gray800};
  `,

  // ── Bayesian Update: section heading with tag ──
  sectionHeadingRow: css`
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0;
  `,
  tagBadge: css`
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 999px;
    background-color: ${COLORS.gray100};
    border: 1px solid ${COLORS.gray300};
    font-size: 11px;
    font-weight: 500;
    color: ${COLORS.gray600};
    white-space: nowrap;
  `,

  // ── Bayesian Update: Number of tests lock/unlock ──
  lockedInputRow: css`
    display: flex;
    gap: 8px;
    align-items: center;
  `,
  lockedInputWrapper: css`
    position: relative;
    flex: 1;
  `,
  lockIcon: css`
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 12px;
    pointer-events: none;
  `,
  lockedInputBox: css`
    background-color: ${COLORS.gray100};
    color: ${COLORS.gray500};
    cursor: not-allowed;
    padding-right: 30px;
    &:focus {
      border-color: ${COLORS.gray300};
      box-shadow: none;
    }
  `,
  lockBtn: css`
    flex-shrink: 0;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid ${COLORS.gray300};
    background-color: ${COLORS.white};
    color: ${COLORS.gray600};
    font-size: ${FONT_SIZE.xs};
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
    transition: background-color 0.2s, border-color 0.2s;
    &:hover {
      background-color: ${COLORS.gray50};
      border-color: ${COLORS.gray400};
    }
  `,
  restoreBtn: css`
    flex-shrink: 0;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #f59e0b;
    background-color: #fffbeb;
    color: #b45309;
    font-size: ${FONT_SIZE.xs};
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
    transition: background-color 0.2s;
    &:hover {
      background-color: #fef3c7;
    }
  `,
  hintText: css`
    font-size: 11px;
    color: ${COLORS.gray400};
    margin-top: 2px;
  `,
  warningHintText: css`
    font-size: 11px;
    color: #b45309;
    margin-top: 2px;
  `,
  sectionDescription: css`
    font-size: ${FONT_SIZE.xs};
    color: ${COLORS.gray500};
    margin: 0;
    line-height: 1.5;
  `,

  // ── Result Summary panel ──
  resultSummaryHeader: css`
    display: flex;
    align-items: center;
    justify-content: space-between;
    span {
      font-size: ${FONT_SIZE.base};
      font-weight: 600;
      color: ${COLORS.gray800};
    }
  `,
  jsonDownloadBtn: css`
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid ${COLORS.gray300};
    background-color: ${COLORS.white};
    color: ${COLORS.gray600};
    font-size: ${FONT_SIZE.xs};
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
    &:hover:not(:disabled) {
      background-color: ${COLORS.gray50};
      border-color: ${COLORS.gray400};
    }
    &:disabled {
      cursor: not-allowed;
      opacity: 0.4;
    }
  `,
  resultCardGrid: css`
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    flex: 1;
  `,
  resultCard: css`
    background-color: ${COLORS.gray50};
    border: 1px solid ${COLORS.gray200};
    border-radius: 6px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  `,
  resultCardLabel: css`
    font-size: 11px;
    color: ${COLORS.gray500};
    font-weight: 500;
  `,
  resultCardValue: css`
    font-size: ${FONT_SIZE.base};
    font-weight: 600;
    color: ${COLORS.gray800};
  `,
  // ── Footer note ──
  footerNote: css`
    width: 90%;
    max-width: 1200px;
    text-align: right;
    font-size: ${FONT_SIZE.xs};
    color: ${COLORS.gray500};
    margin-top: 12px;
  `,
};
