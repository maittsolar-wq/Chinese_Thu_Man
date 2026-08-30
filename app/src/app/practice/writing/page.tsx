import type { Metadata } from "next";
import { PracticeConfigView } from "@/components/practice/PracticeConfigView";

export const metadata: Metadata = { title: "Luyện viết — Chinese Thu Man" };

export default function PracticeWritingConfigPage() {
  return <PracticeConfigView practiceType="writing" />;
}
