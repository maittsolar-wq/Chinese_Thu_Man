import type { Metadata } from "next";
import { PracticeConfigView } from "@/components/practice/PracticeConfigView";

export const metadata: Metadata = { title: "Chọn nghĩa — Chinese Thu Man" };

export default function PracticeMeaningConfigPage() {
  return <PracticeConfigView practiceType="meaning" />;
}
