import type { Metadata } from "next";
import Link from "next/link";
import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { BookOpenIcon, TargetIcon, UserIcon } from "@/components/ui/icons";
import { PRACTICE_CARDS, PRACTICE_CARD_ACCENT_STYLES, practiceRoute } from "@/lib/practice/types";

export const metadata: Metadata = { title: "Luyện tập — Chinese Thu Man" };

/**
 * Informational-only content (P4.2 §3). These are plain text blocks, not
 * entry points — no href, no onClick, rendered as bare <Card>/<div> (see
 * components/ui/Card.tsx) so there is no interactive affordance at all,
 * unlike the 4 practice cards below which are real navigations. Icon
 * badges reuse PRACTICE_CARD_ACCENT_STYLES (already defined for the
 * practice cards) rather than a second color map.
 */
const PRACTICE_INFO_ITEMS = [
  {
    title: "Ôn tập thông minh",
    description: "Hệ thống sẽ ưu tiên các từ bạn chưa thuộc và trả lời sai.",
    icon: BookOpenIcon,
    accent: "blue",
  },
  {
    title: "Cá nhân hóa",
    description: "Bài tập phù hợp với trình độ của bạn",
    icon: UserIcon,
    accent: "green",
  },
  {
    title: "Theo dõi tiến độ",
    description: "Giúp bạn thấy sự tiến bộ mỗi ngày",
    icon: TargetIcon,
    accent: "purple",
  },
  {
    title: "Học mọi lúc mọi nơi",
    description: "Luyện tập nhanh chóng trên mọi thiết bị",
    icon: BookOpenIcon,
    accent: "red",
  },
] as const;

/**
 * Standalone Practice Home (P4.2) — the 4 cards below are the SAME
 * PRACTICE_CARDS data and practiceRoute() navigation Home's embedded
 * #luyen-tap section already used (see app/src/app/page.tsx), now hoisted
 * into lib/practice/types.ts so this page and Home share one definition
 * instead of two. No exercise flow, session logic, or data-fetching is
 * reimplemented here — every card link resolves to the existing, already
 * functional /practice/{meaning,character,flashcard,writing} routes.
 *
 * Visual details (title casing/size, card padding/icon treatment, the
 * info section's single outer border) match the approved UI reference
 * screenshot supplied for this page.
 */
export default function PracticeHomePage() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-2">
        <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Luyện tập" }]} />
        <h1 className="mt-4 text-3xl font-extrabold uppercase tracking-wide text-primary sm:text-4xl">
          Luyện tập
        </h1>
        <p className="text-sm text-neutral-600 dark:text-night-muted">
          Học từ vựng theo 6 cấp độ HSK từ cơ bản đến nâng cao.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {PRACTICE_CARDS.map((card) => {
          const style = PRACTICE_CARD_ACCENT_STYLES[card.accent];
          return (
            <Link key={card.title} href={practiceRoute(card.type)} className="block min-w-0">
              <Card
                className={clsx(
                  "flex items-start gap-4 border-2 p-6 hover:shadow-md",
                  style.border
                )}
              >
                <card.icon className={clsx("h-9 w-9 shrink-0", style.icon)} />
                <div className="flex min-w-0 flex-col gap-1">
                  <span className={clsx("text-xl font-bold", style.icon)}>{card.title}</span>
                  <span className={clsx("text-sm", style.icon)}>{card.description}</span>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>

      <Card className="border-2 border-primary p-6 sm:p-8">
        <div className="grid gap-6 sm:grid-cols-2">
          {PRACTICE_INFO_ITEMS.map((item) => {
            const style = PRACTICE_CARD_ACCENT_STYLES[item.accent];
            return (
              <div key={item.title} className="flex items-start gap-3">
                <span
                  className={clsx(
                    "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg",
                    style.badgeBg,
                    style.icon
                  )}
                >
                  <item.icon className="h-5 w-5" />
                </span>
                <div className="flex min-w-0 flex-col">
                  <span className="text-base font-semibold text-neutral-900 dark:text-night-text">
                    {item.title}
                  </span>
                  <span className="text-sm text-neutral-600 dark:text-night-muted">
                    {item.description}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
