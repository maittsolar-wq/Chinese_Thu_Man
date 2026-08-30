import type { Metadata } from "next";
import { MeaningPracticeFlow } from "@/components/practice/MeaningPracticeFlow";

export const metadata: Metadata = { title: "Chọn nghĩa — Chinese Thu Man" };

export default function PracticeMeaningConfigPage() {
  return <MeaningPracticeFlow />;
}
