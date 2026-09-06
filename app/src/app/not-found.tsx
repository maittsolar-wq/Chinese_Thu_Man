import { LinkButton } from "@/components/ui/Button";
import { ArrowRightIcon } from "@/components/ui/icons";

/**
 * Phase 07: previously a bare EmptyState (a component designed for an
 * inline "no results in this list" message, not a dedicated full page) —
 * given real page presence (a proper heading, centered, more vertical
 * room) while still using only the approved design system: primary blue,
 * the existing neutral ramp, no new illustration.
 */
export default function NotFound() {
  return (
    <div className="flex flex-col items-center gap-3 py-20 text-center">
      <p className="font-data text-sm font-semibold uppercase tracking-wide text-neutral-500 dark:text-night-muted">
        404
      </p>
      <h1 className="text-2xl font-bold text-primary dark:text-night-primary">
        Không tìm thấy nội dung
      </h1>
      <p className="max-w-sm text-sm text-neutral-600 dark:text-night-muted">
        Nội dung bạn tìm không tồn tại hoặc đã bị thay đổi.
      </p>
      <LinkButton href="/" className="mt-2">
        Về trang chủ
        <ArrowRightIcon className="h-4 w-4" />
      </LinkButton>
    </div>
  );
}
