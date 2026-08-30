import type { Metadata } from "next";
import { WritingPracticeFlow } from "@/components/practice/WritingPracticeFlow";

export const metadata: Metadata = { title: "Luyện viết — Chinese Thu Man" };

export default function PracticeWritingConfigPage() {
  return <WritingPracticeFlow />;
}
