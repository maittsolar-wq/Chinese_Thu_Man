import type { Metadata } from "next";
import { PracticeConfigView } from "@/components/practice/PracticeConfigView";

export const metadata: Metadata = { title: "Flashcard — Chinese Thu Man" };

export default function PracticeFlashcardConfigPage() {
  return <PracticeConfigView practiceType="flashcard" />;
}
