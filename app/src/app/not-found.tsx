import { EmptyState } from "@/components/ui/EmptyState";
import { LinkButton } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <EmptyState
      title="Không tìm thấy nội dung"
      description="Nội dung bạn tìm không tồn tại hoặc đã bị thay đổi."
      action={<LinkButton href="/">Về trang chủ</LinkButton>}
    />
  );
}
