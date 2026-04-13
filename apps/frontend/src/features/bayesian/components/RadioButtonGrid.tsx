import { useRef, useState, useEffect } from 'react';

interface RadioItem {
  label: string;
  uniqueKey: string;
  value: string;
  onChange: (value: string) => void;
}

const OPTIONS = ['High', 'Medium', 'Low'] as const;

const OPTION_COLORS: Record<string, { active: string; activeBg: string; hoverBg: string }> = {
  High:   { active: '#15803d', activeBg: '#dcfce7', hoverBg: '#f0fdf4' },
  Medium: { active: '#b45309', activeBg: '#fef3c7', hoverBg: '#fffbeb' },
  Low:    { active: '#b91c1c', activeBg: '#fee2e2', hoverBg: '#fef2f2' },
};

function SegmentedRow({ item }: { item: RadioItem }) {
  const [hovered, setHovered] = useState<string | null>(null);

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '12px',
      padding: '8px 12px',
      borderRadius: '8px',
    }}>
      <span style={{ fontSize: '14px', color: '#374151', lineHeight: '1.4', flex: 1 }}>
        {item.label}
      </span>
      <div style={{
        display: 'flex',
        border: '1px solid #d1d5db',
        borderRadius: '8px',
        overflow: 'hidden',
        flexShrink: 0,
      }}>
        {OPTIONS.map((opt, idx) => {
          const checked = item.value === opt;
          const { active, activeBg, hoverBg } = OPTION_COLORS[opt];
          const isHovered = hovered === opt;
          return (
            <button
              key={opt}
              onClick={() => item.onChange(opt)}
              onMouseEnter={() => setHovered(opt)}
              onMouseLeave={() => setHovered(null)}
              style={{
                padding: '5px 14px',
                fontSize: '13px',
                fontWeight: checked ? 600 : 400,
                cursor: 'pointer',
                border: 'none',
                borderLeft: idx > 0 ? '1px solid #d1d5db' : 'none',
                backgroundColor: checked ? activeBg : isHovered ? hoverBg : '#ffffff',
                color: checked ? active : '#6b7280',
                transition: 'background-color 0.1s, color 0.1s',
              }}
            >
              {opt}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function SegmentedPanel({ items }: { items: RadioItem[] }) {
  return (
    <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {items.map((item, idx) => (
        <div key={item.uniqueKey} style={{ backgroundColor: idx % 2 === 0 ? '#f9fafb' : '#ffffff', borderRadius: '8px' }}>
          <SegmentedRow item={item} />
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
      <div ref={containerRef} style={{ display: 'flex', gap: '24px', alignItems: 'flex-start' }}>
        {isNarrow ? (
          <SegmentedPanel items={items} />
        ) : (
          <>
            <SegmentedPanel items={col1} />
            {col2.length > 0 && <SegmentedPanel items={col2} />}
          </>
        )}
      </div>
    </div>
  );
}
