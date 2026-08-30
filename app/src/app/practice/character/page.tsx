import type { Metadata } from "next";
import { ChoicePracticeFlow } from "@/components/practice/ChoicePracticeFlow";

export const metadata: Metadata = { title: "Chọn chữ Hán — Chinese Thu Man" };

export default function PracticeCharacterConfigPage() {
  return <ChoicePracticeFlow practiceType="character" />;
}
