import type { Metadata } from "next";
import { ListeningHero } from "@/components/listening/ListeningHero";
import { ListeningLevelCards } from "@/components/listening/ListeningLevelCards";
import { ListeningBenefits } from "@/components/listening/ListeningBenefits";

export const metadata: Metadata = { title: "Luyện nghe — Chinese Thu Man" };

/**
 * The bottom CTA card ("Nghe nhiều hơn / Hiểu sâu hơn / Tiến bộ mỗi ngày")
 * that previously closed this page has been removed per the approved UI
 * finalization pass — it is no longer part of the approved Listening
 * Landing design. The page now ends after Benefits and flows straight into
 * the site's shared Footer (rendered once in the root layout).
 */
export default function ListeningLandingPage() {
  return (
    <div className="flex flex-col gap-14">
      <ListeningHero />
      <ListeningLevelCards />
      <ListeningBenefits />
    </div>
  );
}
