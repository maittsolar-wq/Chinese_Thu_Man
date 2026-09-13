import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

const base = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 2,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export function HomeIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M3 11.5 12 4l9 7.5" />
      <path d="M5 10v9a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-9" />
    </svg>
  );
}

export function GraduationCapIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="m2 9 10-5 10 5-10 5-10-5Z" />
      <path d="M6 11v5c0 1.1 2.7 2 6 2s6-.9 6-2v-5" />
      <path d="M22 9v6" />
    </svg>
  );
}

export function SearchIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-3.5-3.5" />
    </svg>
  );
}

export function TargetIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="12" r="9" />
      <circle cx="12" cy="12" r="5" />
      <circle cx="12" cy="12" r="1" />
    </svg>
  );
}

export function MoonIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z" />
    </svg>
  );
}

export function SunIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
    </svg>
  );
}

export function RadicalIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="3.5" y="3.5" width="7.5" height="7.5" rx="1.2" />
      <rect x="13" y="3.5" width="7.5" height="7.5" rx="1.2" />
      <rect x="3.5" y="13" width="7.5" height="7.5" rx="1.2" />
      <rect x="13" y="13" width="7.5" height="7.5" rx="1.2" />
    </svg>
  );
}

export function ArrowRightIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M5 12h14M13 6l6 6-6 6" />
    </svg>
  );
}

export function BookOpenIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M12 6.5c-1.6-1-4-1.5-6-1.5-1 0-2 .1-3 .4v13c1-.3 2-.4 3-.4 2 0 4.4.5 6 1.5" />
      <path d="M12 6.5c1.6-1 4-1.5 6-1.5 1 0 2 .1 3 .4v13c-1-.3-2-.4-3-.4-2 0-4.4.5-6 1.5V6.5Z" />
    </svg>
  );
}

export function CardsIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="7" y="8" width="14" height="12" rx="2" />
      <path d="M4.5 15.5V5a1 1 0 0 1 1-1H15" />
    </svg>
  );
}

export function PencilIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M4 20h4L18.5 9.5a2.1 2.1 0 0 0-3-3L5 17v3Z" />
      <path d="M13.5 6.5l3 3" />
    </svg>
  );
}

export function ArrowLeftIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M19 12H5M11 6l-6 6 6 6" />
    </svg>
  );
}

export function ChevronDownIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

export function ChevronLeftIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="m15 6-6 6 6 6" />
    </svg>
  );
}

export function ChevronRightIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="m9 6 6 6-6 6" />
    </svg>
  );
}

export function SpeakerIcon(props: IconProps) {
  return (
    <svg {...base} fill="currentColor" stroke="none" {...props}>
      <path d="M4 9v6h4l5 4V5L8 9H4Z" />
      <path
        d="M16.5 8.5a5 5 0 0 1 0 7"
        fill="none"
        stroke="currentColor"
        strokeWidth={2}
        strokeLinecap="round"
      />
    </svg>
  );
}

export function CloseIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M6 6l12 12M18 6 6 18" />
    </svg>
  );
}

export function LightbulbIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M9 18h6M10 21h4" />
      <path d="M12 3a6 6 0 0 0-3.5 10.9c.6.45.9 1.02.9 1.6h5.2c0-.58.3-1.15.9-1.6A6 6 0 0 0 12 3Z" />
    </svg>
  );
}

/**
 * Custom Practice Home card icons (P4.2 final icon pass) — more detailed
 * than the generic Search/BookOpen/Cards/Pencil icons above (which stay
 * unchanged; they're still used elsewhere: header nav, HSK page, etc.),
 * built to visually match the approved Practice Home reference screenshot
 * more closely while following this file's exact stroke conventions
 * (`base`: 24x24 viewBox, currentColor stroke, width 2, round caps/joins).
 * "A-Z" is represented abstractly as short text-line marks rather than
 * literal letterforms — legible at small icon scale, same idea as the
 * reference's alphabetical/word-list visual.
 */
export function PracticeMeaningIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="9" cy="9" r="6" />
      <path d="M6.5 7.3h5M6.5 9.6h3.6M6.5 11.9h4.6" />
      <path d="M13.4 13.4 20 20" />
    </svg>
  );
}

export function PracticeCharacterIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M12 6.5c-1.6-1-4-1.5-6-1.5-1 0-2 .1-3 .4v13c1-.3 2-.4 3-.4 2 0 4.4.5 6 1.5" />
      <path d="M12 6.5c1.6-1 4-1.5 6-1.5 1 0 2 .1 3 .4v13c-1-.3-2-.4-3-.4-2 0-4.4.5-6 1.5V6.5Z" />
      <path d="M4.8 8.7h3.4M4.8 11.2h2.8" />
      <path d="M14.8 8.7h3.4M15.3 11.2h2.6" />
    </svg>
  );
}

export function PracticeFlashcardIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="3" y="2" width="13" height="17" rx="2" />
      <rect x="8" y="6" width="13" height="17" rx="2" />
      <path d="M11 14.5h7" />
    </svg>
  );
}

export function PracticeWritingIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <rect x="3" y="2" width="13" height="17" rx="1.5" />
      <path d="M5.5 7h7.5M5.5 10.5h7.5M5.5 14h4.5" />
      {/* Same shape as PencilIcon above, scaled ~0.85x and repositioned to
          sit beside the notepad rather than fill the whole viewBox — kept
          identical in style/proportion to the proven standalone icon. */}
      <path d="M11 20.5h3.4L23.3 11.55a1.8 1.8 0 0 0-2.5-2.55L11.9 17.9v2.6Z" />
      <path d="M19.1 9l2.6 2.6" />
    </svg>
  );
}

export function UserIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 20c0-3.9 3.6-7 8-7s8 3.1 8 7" />
    </svg>
  );
}

export function ReplayIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
    </svg>
  );
}

/**
 * Practice Config redesign pass — "Số lượng từ" section header icon. No
 * existing icon in this file represents a bar-chart/quantity concept, and
 * this app's own convention is hand-authored inline SVGs (not an icon
 * library dependency) following the exact `base` stroke spec every icon
 * above already uses, so this is one more of those, not a new dependency.
 */
export function BarChartIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M4 20V10M12 20V4M20 20v-7" />
    </svg>
  );
}

export function CheckCircleIcon(props: IconProps) {
  return (
    <svg {...base} fill="currentColor" stroke="none" {...props}>
      <circle cx="12" cy="12" r="10" />
      <path
        d="m8.5 12.2 2.4 2.4 4.6-4.9"
        fill="none"
        stroke="white"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

/**
 * Listening feature icon set (V1 UI phase) — follows the exact same
 * hand-authored inline SVG convention as every icon above (24x24 viewBox,
 * `base` stroke spec unless a filled glyph is explicitly called for, e.g.
 * Play/Pause/Heart-filled matching CheckCircleIcon's own filled precedent).
 */
export function HeadphonesIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M4 13v-1a8 8 0 0 1 16 0v1" />
      <rect x="3" y="13" width="5" height="7" rx="1.5" />
      <rect x="16" y="13" width="5" height="7" rx="1.5" />
    </svg>
  );
}

export function PlayIcon(props: IconProps) {
  return (
    <svg {...base} fill="currentColor" stroke="none" {...props}>
      <path d="M7 4.5v15l13-7.5-13-7.5Z" />
    </svg>
  );
}

export function PauseIcon(props: IconProps) {
  return (
    <svg {...base} fill="currentColor" stroke="none" {...props}>
      <rect x="6" y="4.5" width="4.5" height="15" rx="1" />
      <rect x="13.5" y="4.5" width="4.5" height="15" rx="1" />
    </svg>
  );
}

export function HeartIcon({ filled, ...props }: IconProps & { filled?: boolean }) {
  return (
    <svg
      {...base}
      fill={filled ? "currentColor" : "none"}
      stroke={filled ? "none" : "currentColor"}
      {...props}
    >
      <path d="M12 20.5s-7.5-4.6-9.8-9.2C.6 7.9 2.3 4.5 5.7 4c2-.3 3.9.7 6.3 3 2.4-2.3 4.3-3.3 6.3-3 3.4.5 5.1 3.9 3.5 7.3-2.3 4.6-9.8 9.2-9.8 9.2Z" />
    </svg>
  );
}

export function SkipBackIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M13 6 6 12l7 6V6Z" />
      <path d="M18 6v12" />
    </svg>
  );
}

export function SkipForwardIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M11 6l7 6-7 6V6Z" />
      <path d="M6 6v12" />
    </svg>
  );
}

export function ExpandIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M9 4H4v5M15 4h5v5M9 20H4v-5M15 20h5v-5" />
    </svg>
  );
}

export function GearIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1Z" />
    </svg>
  );
}

export function MessageListIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <path d="M4 5.5h16M4 12h11M4 18.5h16" />
    </svg>
  );
}

export function ClockIcon(props: IconProps) {
  return (
    <svg {...base} {...props}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3.5 2" />
    </svg>
  );
}
