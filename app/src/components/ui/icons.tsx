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
