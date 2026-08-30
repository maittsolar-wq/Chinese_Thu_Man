import type { Metadata } from "next";
import { ChoicePracticeFlow } from "@/components/practice/ChoicePracticeFlow";

export const metadata: Metadata = { title: "Chọn nghĩa — Chinese Thu Man" };

export default function PracticeMeaningConfigPage() {
  return <ChoicePracticeFlow practiceType="meaning" />;
}
