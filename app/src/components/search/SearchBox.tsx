export function SearchBox({ defaultValue }: { defaultValue?: string }) {
  return (
    <form action="/dictionary" method="get" className="flex w-full gap-2">
      <input
        type="text"
        name="q"
        defaultValue={defaultValue}
        placeholder="Nhập chữ Hán, pinyin hoặc nghĩa tiếng Việt..."
        className="w-full min-w-0 rounded-md border border-neutral-300 px-4 py-2.5 text-base text-neutral-900 outline-none focus:border-primary focus:ring-1 focus:ring-primary"
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
