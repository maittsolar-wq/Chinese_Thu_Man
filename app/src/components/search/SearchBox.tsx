export function SearchBox({
  defaultValue,
  placeholder = "Nhập chữ Hán, pinyin hoặc nghĩa tiếng Việt...",
}: {
  defaultValue?: string;
  placeholder?: string;
}) {
  return (
    <form action="/dictionary" method="get" className="flex w-full gap-2">
      <input
        type="text"
        name="q"
        defaultValue={defaultValue}
        placeholder={placeholder}
        className="w-full min-w-0 rounded-md border border-neutral-300 bg-white px-4 py-2.5 text-base text-neutral-900 outline-none placeholder:text-neutral-500 focus:border-primary focus:ring-1 focus:ring-primary dark:border-night-border dark:bg-night-input dark:text-night-text dark:placeholder:text-night-muted"
        aria-label="Tìm kiếm từ vựng"
      />
      <button
        type="submit"
        className="shrink-0 rounded-md bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-dark"
      >
        Tìm kiếm
      </button>
    </form>
  );
}
