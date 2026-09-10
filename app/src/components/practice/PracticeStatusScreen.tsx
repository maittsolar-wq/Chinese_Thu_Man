import { LinkButton } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { ArrowLeftIcon } from "@/components/ui/icons";

/**
 * The "loading" and "empty" phases were identical, byte-for-byte JSX
 * duplicated three times across ChoicePracticeFlow, FlashcardPracticeFlow,
 * and WritingPracticeFlow (Phase 05 audit) — consolidated here as one
 * presentational component so the three flows can't visually drift from
 * each other. Carries no session-shape awareness and makes no state
 * transitions itself; each flow still owns its own phase state exactly as
 * before, this is a pure render helper.
 */
export function PracticeStatusScreen({
  variant,
}: {
  variant: "loading" | "empty";
}) {
  return (
    <div className="flex flex-col gap-6">
      <LinkButton href="/" variant="neutral" className="font-ui h-12 w-fit rounded-xl px-6">
        <ArrowLeftIcon className="h-4 w-4" />
        Quay lại
      </LinkButton>
      {variant === "loading" ? (
        <EmptyState title="Đang chuẩn bị bài luyện tập..." />
      ) : (
        <EmptyState
          title="Không có từ vựng cho cấp độ này."
          description="Vui lòng quay lại và chọn cấp độ HSK khác."
        />
      )}
    </div>
  );
}
