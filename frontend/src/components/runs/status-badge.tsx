import { Badge } from "@/components/ui/badge";
import { RunStatus, ResultStatus } from "@/types";

const VARIANT: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  passed: "default",
  completed: "default",
  failed: "destructive",
  error: "destructive",
  running: "secondary",
  pending: "secondary",
  skipped: "outline",
};

export function StatusBadge({ status }: { status: RunStatus | ResultStatus }) {
  return <Badge variant={VARIANT[status] ?? "outline"}>{status}</Badge>;
}
