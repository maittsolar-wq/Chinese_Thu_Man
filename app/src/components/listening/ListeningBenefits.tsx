import { MessageListIcon, BookOpenIcon, GraduationCapIcon, HeadphonesIcon } from "@/components/ui/icons";
import type { ComponentType, SVGProps } from "react";

/**
 * `accent` reuses the existing `accent.*` Tailwind tokens (tailwind.config.ts
 * — the same palette Practice's own cards already draw from, see
 * PRACTICE_CARD_ACCENT_STYLES in lib/practice/types.ts) at low opacity for
 * the icon circle, one distinct color per item per the approved reference
 * — not a new color system.
 */
const BENEFITS: {
  icon: ComponentType<SVGProps<SVGSVGElement>>;
  title: string;
  description: string;
  accent: "green" | "blue" | "orange" | "purple";
}[] = [
  {
    icon: MessageListIcon,
    title: "Hội thoại thực tế và tự nhiên",
    description: "Các tình huống gần gũi trong cuộc sống",
    accent: "green",
  },
  {
    icon: BookOpenIcon,
    title: "Có phụ đề, pinyin, nghĩa tiếng Việt",
    description: "Hỗ trợ học hiểu tốt hơn (trong video)",
    accent: "blue",
  },
  {
    icon: GraduationCapIcon,
    title: "Lộ trình theo cấp độ HSK",
    description: "Học từ cơ bản đến nâng cao",
    accent: "orange",
  },
  {
    icon: HeadphonesIcon,
    title: "Luyện nghe mọi lúc, mọi nơi",
    description: "Trên máy tính, điện thoại, máy tính bảng",
    accent: "purple",
  },
];

const ACCENT_CLASSES: Record<(typeof BENEFITS)[number]["accent"], string> = {
  green: "bg-accent-green/10 text-accent-green dark:bg-accent-green/20",
  blue: "bg-accent-blue/10 text-accent-blue dark:bg-accent-blue/20",
  orange: "bg-accent-orange/10 text-accent-orange dark:bg-accent-orange/20",
  purple: "bg-accent-purple/10 text-accent-purple dark:bg-accent-purple/20",
};

/**
 * Pure marketing/feature copy — no subtitle toggle or any other real
 * control is implemented here, per the explicit "this is copy only" scope
 * note: the actual mock video already has Chinese + pinyin + Vietnamese
 * baked in.
 */
export function ListeningBenefits() {
  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {BENEFITS.map(({ icon: Icon, title, description, accent }) => (
        <div
          key={title}
          className="flex flex-col items-center gap-2 rounded-2xl border border-[#E2E8F0] bg-white p-5 text-center dark:border-night-border dark:bg-night-surface"
        >
          <span className={`flex h-11 w-11 items-center justify-center rounded-full ${ACCENT_CLASSES[accent]}`}>
            <Icon className="h-5 w-5" />
          </span>
          <p className="font-ui text-base font-semibold leading-snug text-[#0F172A] dark:text-night-text">
            {title}
          </p>
          <p className="font-ui text-sm leading-snug text-neutral-500 dark:text-night-muted">{description}</p>
        </div>
      ))}
    </section>
  );
}
