import type { Metadata } from "next";
import Link from "next/link";
import clsx from "clsx";
import { Card } from "@/components/ui/Card";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { ArrowRightIcon } from "@/components/ui/icons";
import { PRACTICE_CARDS, PRACTICE_CARD_ACCENT_STYLES, practiceRoute } from "@/lib/practice/types";

export const metadata: Metadata = { title: "Luyện tập — Chinese Thu Man" };

/**
 * Practice landing (Phase 05 redesign). Previously: a 4-card grid plus a
 * second bordered panel of four marketing claims ("Ôn tập thông minh",
 * "Theo dõi tiến độ", ...) that nothing in the product actually backs — no
 * spaced-repetition/priority-review system and no progress persistence
 * exist anywhere in lib/practice (verified directly against every session
 * file). Removed rather than reworded, per this phase's explicit
 * instruction not to invent progress/statistics that don't exist. The four
 * real exercise types remain the entire page, each with a concrete
 * "what you'll do" description and an explicit entry action.
 */
export default function PracticeHomePage() {
  return (
    <div className="flex flex-col gap-6">
      <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Luyện tập" }]} />

      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-bold text-primary dark:text-night-primary">Luyện tập</h1>
        <p className="text-sm text-neutral-600 dark:text-night-muted">
          Chọn một hình thức để ôn lại từ vựng đã học.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {PRACTICE_CARDS.map((card) => {
          const style = PRACTICE_CARD_ACCENT_STYLES[card.accent];
          return (
            <Link key={card.title} href={practiceRoute(card.type)} className="group block min-w-0">
              <Card className={clsx("flex h-full items-start gap-4 border-2 p-6 hover:shadow-md", style.border)}>
                <card.icon className={clsx("h-9 w-9 shrink-0", style.icon)} />
                <div className="flex min-w-0 flex-1 flex-col gap-1">
                  <span className={clsx("text-xl font-bold", style.icon)}>{card.title}</span>
                  <span className="text-sm text-neutral-600 dark:text-night-muted">
                    {card.description}
                  </span>
                  <span
                    className={clsx(
                      "mt-2 inline-flex w-fit items-center gap-1 text-sm font-semibold transition-colors",
                      style.icon
                    )}
                  >
                    Bắt đầu
                    <ArrowRightIcon className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                  </span>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
