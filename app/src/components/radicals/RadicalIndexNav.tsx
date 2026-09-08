"use client";

import { useEffect, useState } from "react";
import { Breadcrumb } from "@/components/ui/Breadcrumb";
import { LinkButton } from "@/components/ui/Button";
import { ArrowLeftIcon } from "@/components/ui/icons";

/**
 * Navigation-completion pass: Radical Index is a child screen when
 * reached through Home's or HSK's own "214 bộ thủ" CTA (`?from=home` /
 * `?from=hsk`) — those flows get the same "Quay lại" Back button pattern
 * used everywhere else in this navigation chain, replacing the
 * "Trang chủ > Bộ thủ" breadcrumb. Direct/bookmarked `/radicals` (no
 * `from`, or an unrecognized one) keeps its original, unchanged canonical
 * breadcrumb — that's the safe-fallback case, not a Back button.
 */
function resolveBackHref(from: string | null): string | null {
  if (from === "home") return "/";
  if (from === "hsk") return "/hsk";
  return null;
}

/**
 * Reads `?from=` via window.location.search rather than useSearchParams()
 * — same reasoning as AppHeader's own source-context read: keeps
 * /radicals a plain static (○) page instead of opting it into dynamic
 * rendering just for a Back button. Defaults to the breadcrumb (the
 * canonical, most common direct-access shape) until the effect resolves,
 * then swaps to the Back button if `from` says so — the same one-frame-
 * late tradeoff AppHeader itself already accepts for its active-tab
 * highlight.
 */
export function RadicalIndexNav() {
  const [backHref, setBackHref] = useState<string | null>(null);

  useEffect(() => {
    const from = new URLSearchParams(window.location.search).get("from");
    setBackHref(resolveBackHref(from));
  }, []);

  if (backHref) {
    return (
      <LinkButton href={backHref} variant="neutral" className="font-ui w-fit">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>
    );
  }

  return <Breadcrumb items={[{ label: "Trang chủ", href: "/" }, { label: "Bộ thủ" }]} />;
}
