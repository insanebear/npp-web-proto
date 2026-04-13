/** @jsxImportSource @emotion/react */
import { cssObj } from "./style";
import type { ChangeEvent } from "react";

export type SettingsFormValues = {
  nChains: number;
  nIter: number;
  nBurnin: number;
  nThin: number;
};

const settingsFields: { label: string; key: keyof SettingsFormValues }[] = [
  { label: "Number of Chains", key: "nChains" },
  { label: "Number of Iterations", key: "nIter" },
  { label: "Number of Burns", key: "nBurnin" },
  { label: "Thinning Rate", key: "nThin" },
];

export default function SettingsForm({
  values,
  onChange,
}: {
  values: SettingsFormValues;
  onChange: (key: keyof SettingsFormValues, value: number) => void;
}) {
  const handleChange = (e: ChangeEvent<HTMLInputElement>, key: keyof SettingsFormValues) => {
    onChange(key, Number(e.target.value));
  };

  return (
    <div css={cssObj.embeddedWrapper}>
      <main css={cssObj.mainContent}>
        <section id="settings-title-section" css={[cssObj.container, cssObj.settingsTitleSection]}>
          <h1 css={cssObj.title}>BBN Hyperparameters</h1>
        </section>
        <section css={cssObj.settingsGrid}>
          {settingsFields.map(({ label, key }) => (
            <div key={key} css={cssObj.settingBox}>
              <label htmlFor={key} css={cssObj.inputLabel}>{label}</label>
              <input
                type="number"
                id={key}
                value={String(values[key])}
                onChange={(e) => handleChange(e, key)}
                css={cssObj.inputBox}
              />
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
