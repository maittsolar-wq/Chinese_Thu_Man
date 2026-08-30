import type { Metadata } from "next";
import { FlashcardPracticeFlow } from "@/components/practice/FlashcardPracticeFlow";

export const metadata: Metadata = { title: "Flashcard — Chinese Thu Man" };

export default function PracticeFlashcardConfigPage() {
  return <FlashcardPracticeFlow />;
}
