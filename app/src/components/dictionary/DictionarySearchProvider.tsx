"use client";

import { createContext, useCallback, useContext, useMemo, useState } from "react";

/**
 * Shared open/close state for the ONE DictionarySearchPopup instance,
 * mounted once in layout.tsx (see the "preferred architecture" diagram:
 * Header trigger and Home trigger both call the same open()). Neither
 * trigger nor the popup owns this state itself, so there is exactly one
 * popup — never a second, divergent one.
 */
const DictionarySearchContext = createContext<{
  isOpen: boolean;
  open: () => void;
  close: () => void;
} | null>(null);

export function DictionarySearchProvider({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);

  const value = useMemo(() => ({ isOpen, open, close }), [isOpen, open, close]);

  return (
    <DictionarySearchContext.Provider value={value}>{children}</DictionarySearchContext.Provider>
  );
}

export function useDictionarySearch() {
  const ctx = useContext(DictionarySearchContext);
  if (!ctx) throw new Error("useDictionarySearch must be used within a DictionarySearchProvider");
  return ctx;
}
