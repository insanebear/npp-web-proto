import { useRef, useState, useEffect } from 'react';

interface RadioItem {
  label: string;
  uniqueKey: string;
  value: string;
  onChange: (value: string) => void;
}

const OPTIONS = ['High', 'Medium', 'Low'] as const;

function RadioGroupPanel({ items }: { items: RadioItem[] }) {
  return (
    <div style={{ flex: 1, minWidth: 0 }}>
      {/* Header row */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 64px 72px 60px',
        padding: '4px 8px 8px',
        borderBottom: '2px solid #d1d5db',
        marginBottom: '2px',
      }}>
        <div />
        {OPTIONS.map((opt) => (
          <div key={opt} style={{
            textAlign: 'center',
            fontSize: '16px',
            fontWeight: '700',
            color: '#1f2937',
            letterSpacing: '0.03em',
          }}>
            {opt}
          </div>
        ))}
      </div>

      {/* Item rows */}
      {items.map((item, idx) => (
        <div key={item.uniqueKey} style={{
          display: 'grid',
          gridTemplateColumns: '1fr 64px 72px 60px',
          alignItems: 'center',
          padding: '5px 8px',
          backgroundColor: idx % 2 === 0 ? '#f9fafb' : '#ffffff',
          borderRadius: '4px',
        }}>
          <span style={{
            fontSize: '16px',
            color: '#374151',
            paddingRight: '8px',
            lineHeight: '1.3',
          }}>
            {item.label}
          </span>
          {OPTIONS.map((opt) => {
            const checked = item.value === opt;
            return (
              <div key={opt} style={{ display: 'flex', justifyContent: 'center' }}>
                <label style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <input
                    type="radio"
                    name={item.uniqueKey}
                    value={opt}
                    checked={checked}
                    onChange={() => item.onChange(opt)}
                    style={{ position: 'absolute', opacity: 0, width: 0, height: 0, pointerEvents: 'none' }}
                  />
                  <span style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '18px',
                    height: '18px',
                    borderRadius: '50%',
                    border: `2px solid ${checked ? '#2563eb' : '#9ca3af'}`,
                    backgroundColor: checked ? '#2563eb' : '#ffffff',
                    boxSizing: 'border-box',
                    flexShrink: 0,
                  }}>
                    {checked && (
                      <span style={{
                        width: '10px',
                        height: '10px',
                        borderRadius: '50%',
                        backgroundColor: '#ffffff',
                        flexShrink: 0,
                      }} />
                    )}
                  </span>
                </label>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}

interface RadioButtonGridProps {
  children: readonly { label: string; values: readonly string[] }[];
  tabLabel: string;
  inputValues: { [key: string]: string };
  onInputChange: (key: string, value: string) => void;
}

const LEVEL_DESCRIPTIONS = [
  { level: 'High', color: '#15803d', description: 'Exceeds safety standards (IEEE/IEC) with additional reliability-enhancing activities.' },
  { level: 'Medium', color: '#b45309', description: 'Satisfactorily meets all required safety standards with documented evidence.' },
  { level: 'Low', color: '#b91c1c', description: 'Insufficient evidence or unsatisfactory compliance with standards. (Used as the default for conservative assessment)' },
];

export function RadioButtonGrid({ children, tabLabel, inputValues, onInputChange }: RadioButtonGridProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isNarrow, setIsNarrow] = useState(false);
  const [legendOpen, setLegendOpen] = useState(false);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const observer = new ResizeObserver(([entry]) => {
      setIsNarrow(entry.contentRect.width < 640);
    });
    observer.observe(el);
    // Set initial value
    setIsNarrow(el.getBoundingClientRect().width < 640);
    return () => observer.disconnect();
  }, []);

  const items: RadioItem[] = children.map((child) => {
    const uniqueKey = `${tabLabel}/${child.label}`;
    return {
      label: child.label,
      uniqueKey,
      value: inputValues[uniqueKey] || child.values[0],
      onChange: (val: string) => onInputChange(uniqueKey, val),
    };
  });

  const half = Math.ceil(items.length / 2);
  const col1 = items.slice(0, half);
  const col2 = items.slice(half);

  return (
    <div>
      {/* Collapsible legend */}
      <div style={{ marginBottom: '16px' }}>
        <button
          onClick={() => setLegendOpen(o => !o)}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '4px 0',
            color: '#6b7280',
            fontSize: '13px',
          }}
        >
          <span style={{
            display: 'inline-block',
            transform: legendOpen ? 'rotate(90deg)' : 'rotate(0deg)',
            transition: 'transform 0.15s',
            fontSize: '10px',
          }}>▶</span>
          What do these levels mean?
        </button>

        {legendOpen && (
          <div style={{
            marginTop: '8px',
            padding: '12px 16px',
            backgroundColor: '#f9fafb',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}>
            {LEVEL_DESCRIPTIONS.map(({ level, color, description }) => (
              <div key={level} style={{ display: 'flex', gap: '8px', fontSize: '13px', lineHeight: '1.5' }}>
                <span style={{ fontWeight: 700, color, minWidth: '52px' }}>{level}</span>
                <span style={{ color: '#374151' }}>{description}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Grid */}
      <div ref={containerRef} style={{ display: 'flex', gap: '32px', alignItems: 'flex-start' }}>
        {isNarrow ? (
          <RadioGroupPanel items={items} />
        ) : (
          <>
            <RadioGroupPanel items={col1} />
            {col2.length > 0 && <RadioGroupPanel items={col2} />}
          </>
        )}
      </div>
    </div>
  );
}
