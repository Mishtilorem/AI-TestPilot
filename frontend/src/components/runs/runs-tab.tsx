"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { PlayCircle, Loader2 } from "lucide-react";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { useRuns, useStartRun } from "@/hooks/use-runs";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { StatusBadge } from "@/components/runs/status-badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export function RunsTab({ projectId }: { projectId: string }) {
  const router = useRouter();
  const { data: runs, isLoading } = useRuns(projectId);
  const startRun = useStartRun(projectId);
  const [running, setRunning] = useState(false);

  async function onRun() {
    setRunning(true);
    try {
      const run = await startRun.mutateAsync();
      toast.success("Run completed");
      router.push(`/runs/${run.id}`);
    } catch (err) {
      const message =
        err instanceof AxiosError
          ? err.response?.data?.detail ?? "Run failed"
          : "Run failed";
      toast.error(message);
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Runs every test case that has a generated script.
        </p>
        <Button onClick={onRun} disabled={running}>
          {running ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <PlayCircle className="mr-2 h-4 w-4" />
          )}
          {running ? "Running..." : "Run Tests"}
        </Button>
      </div>

      {isLoading ? (
        <Skeleton className="h-32 w-full" />
      ) : runs && runs.length > 0 ? (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Status</TableHead>
              <TableHead>Browser</TableHead>
              <TableHead>Started</TableHead>
              <TableHead className="text-right">Details</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {runs.map((run) => (
              <TableRow key={run.id}>
                <TableCell>
                  <StatusBadge status={run.status} />
                </TableCell>
                <TableCell>{run.browser}</TableCell>
                <TableCell className="text-muted-foreground">
                  {run.start_time ? new Date(run.start_time).toLocaleString() : "—"}
                </TableCell>
                <TableCell className="text-right">
                  <Button variant="outline" size="sm" onClick={() => router.push(`/runs/${run.id}`)}>
                    View
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      ) : (
        <p className="text-sm text-muted-foreground">
          No runs yet. Generate scripts for your test cases, then click Run Tests.
        </p>
      )}
    </div>
  );
}
