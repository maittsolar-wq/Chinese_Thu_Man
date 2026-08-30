import type { Metadata } from "next";
import { PracticeConfigView } from "@/components/practice/PracticeConfigView";

export const metadata: Metadata = { title: "Chọn chữ Hán — Chinese Thu Man" };

export default function PracticeCharacterConfigPage() {
  return <PracticeConfigView practiceType="character" />;
}
