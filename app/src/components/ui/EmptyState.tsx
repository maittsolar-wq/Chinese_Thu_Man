import type { ReactNode } from "react";

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center gap-2 rounded-card border border-dashed border-neutral-300 bg-neutral-50 px-6 py-10 text-center">
      <p className="text-base font-medium text-neutral-800">{title}</p>
      {description && <p className="max-w-sm text-sm text-neutral-600">{description}</p>}
      {action}
    </div>
  );
}
