import Link from "next/link";
import Image from "next/image";
import { ChevronRightIcon } from "@/components/ui/icons";

/**
 * Replaces the old dashboard-style /hsk page's bottom Panel (plain text
 * link "Tra cứu bộ thủ") with the approved reference's CTA card — same
 * `/radicals` route and click behavior, purely a visual upgrade. The
 * "部" icon is the user-supplied asset (public/icons/radical-bo.png),
 * used as-is, not redrawn.
 */
export function RadicalCta() {
  return (
    <Link
      href="/radicals"
      className="group flex flex-col gap-5 rounded-2xl border border-[#E2E8F0] bg-white p-6 transition-colors hover:border-[#015291]/40 dark:border-night-border dark:bg-night-surface sm:flex-row sm:items-center sm:justify-between sm:gap-6"
    >
      <div className="flex items-center gap-4">
        <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-[#0152911A]">
          <Image src="/icons/radical-bo.png" alt="" width={32} height={32} aria-hidden />
        </span>
        <div className="flex flex-col gap-1">
          <h2 className="font-ui text-xl font-bold text-[#0F172A] dark:text-night-text">
            214 Bộ thủ chữ Hán
          </h2>
          <p className="font-ui text-[15px] leading-snug text-[#343536] dark:text-night-muted">
            Mỗi từ vựng đều hiển thị bộ liên quan, giúp bạn hiểu cấu tạo chữ Hán và ghi nhớ dễ dàng hơn.
          </p>
        </div>
      </div>

      <span className="font-ui flex shrink-0 items-center gap-1.5 self-start rounded-full bg-[#015291] px-6 py-3 text-base font-semibold text-white transition-colors group-hover:bg-[#013f70] sm:self-auto">
        Tra cứu bộ thủ
        <ChevronRightIcon className="h-5 w-5" />
      </span>
    </Link>
  );
}
