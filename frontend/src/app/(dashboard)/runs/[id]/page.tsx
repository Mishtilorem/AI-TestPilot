"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Image as ImageIcon, FileText, Sparkles, Loader2, Brain } from "lucide-react";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { useRun } from "@/hooks/use-runs";
import { useTestCases } from "@/hooks/use-test-cases";
import { useAnalyzeFailure } from "@/hooks/use-ai";
import { TestResult } from "@/types";
import { StatusBadge } from "@/components/runs/status-badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export default function RunDetailPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const { data: run, isLoading } = useRun(id);
  const { data: testCases } = useTestCases(run?.project_id ?? "");
  const analyzeFailure = useAnalyzeFailure(id);
  const [logs, setLogs] = useState<string | null>(null);
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<TestResult | null>(null);
  const [analyzingId, setAnalyzingId] = useState<string | null>(null);

  async function onAnalyze(resultId: string) {
    setAnalyzingId(resultId);
    try {
      await analyzeFailure.mutateAsync(resultId);
      toast.success("Analysis ready — click 'AI Analysis' to view");
    } catch (err) {
      const message =
        err instanceof AxiosError
          ? err.response?.data?.detail ?? "Analysis failed"
          : "Analysis failed";
      toast.error(message);
    } finally {
      setAnalyzingId(null);
    }
  }

  if (isLoading || !run) {
    return <Skeleton className="h-60 w-full" />;
  }

  const parsedAnalysis = analysis?.ai_analysis
    ? (JSON.parse(analysis.ai_analysis) as {
        root_cause: string;
        explanation: string;
        possible_fixes: string[];
      })
    : null;

  const titleFor = (r: TestResult) =>
    testCases?.find((tc) => tc.id === r.test_case_id)?.title ?? r.test_case_id.slice(0, 8);

  const passed = run.results.filter((r) => r.status === "passed").length;
  const total = run.results.length;
  const passRate = total > 0 ? Math.round((passed / total) * 100) : 0;

  return (
    <div className="space-y-6">
      <Link
        href={`/projects/${run.project_id}`}
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" /> Back to project
      </Link>

      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-bold">Test Run</h1>
        <StatusBadge status={run.status} />
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Passed</p>
            <p className="text-2xl font-bold">{passed} / {total}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Pass Rate</p>
            <p className="text-2xl font-bold">{passRate}%</p>
            <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-primary transition-all"
                style={{ width: `${passRate}%` }}
              />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Browser</p>
            <p className="text-2xl font-bold capitalize">{run.browser}</p>
          </CardContent>
        </Card>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Test Case</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Duration</TableHead>
            <TableHead className="text-right">Details</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {run.results.map((r) => (
            <TableRow key={r.id}>
              <TableCell className="font-medium">{titleFor(r)}</TableCell>
              <TableCell>
                <StatusBadge status={r.status} />
              </TableCell>
              <TableCell className="text-muted-foreground">
                {r.duration_seconds != null ? `${r.duration_seconds}s` : "—"}
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-1">
                  {r.logs && (
                    <Button variant="outline" size="sm" onClick={() => setLogs(r.logs)}>
                      <FileText className="mr-2 h-4 w-4" /> Logs
                    </Button>
                  )}
                  {r.screenshot_url && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setScreenshot(r.screenshot_url)}
                    >
                      <ImageIcon className="mr-2 h-4 w-4" /> Screenshot
                    </Button>
                  )}
                  {r.status === "failed" &&
                    (r.ai_analysis ? (
                      <Button variant="outline" size="sm" onClick={() => setAnalysis(r)}>
                        <Brain className="mr-2 h-4 w-4" /> AI Analysis
                      </Button>
                    ) : (
                      <Button
                        size="sm"
                        onClick={() => onAnalyze(r.id)}
                        disabled={analyzingId === r.id}
                      >
                        {analyzingId === r.id ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <Sparkles className="mr-2 h-4 w-4" />
                        )}
                        {analyzingId === r.id ? "Analyzing..." : "Analyze"}
                      </Button>
                    ))}
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Dialog open={!!logs} onOpenChange={(open) => !open && setLogs(null)}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Logs</DialogTitle>
          </DialogHeader>
          <pre className="max-h-[60vh] overflow-auto rounded-md bg-muted p-4 text-xs">
            <code>{logs}</code>
          </pre>
        </DialogContent>
      </Dialog>

      <Dialog open={!!screenshot} onOpenChange={(open) => !open && setScreenshot(null)}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Failure Screenshot</DialogTitle>
          </DialogHeader>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          {screenshot && <img src={screenshot} alt="Failure screenshot" className="w-full rounded-md" />}
        </DialogContent>
      </Dialog>

      <Dialog open={!!analysis} onOpenChange={(open) => !open && setAnalysis(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5" /> AI Failure Analysis
            </DialogTitle>
          </DialogHeader>
          {parsedAnalysis && (
            <div className="space-y-4 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">Confidence:</span>
                <Badge>{Math.round((analysis?.ai_confidence ?? 0) * 100)}%</Badge>
              </div>
              <div>
                <p className="font-semibold">Root Cause</p>
                <p className="text-muted-foreground">{parsedAnalysis.root_cause}</p>
              </div>
              <div>
                <p className="font-semibold">Explanation</p>
                <p className="text-muted-foreground">{parsedAnalysis.explanation}</p>
              </div>
              <div>
                <p className="font-semibold">Possible Fixes</p>
                <ul className="list-disc space-y-1 pl-5 text-muted-foreground">
                  {parsedAnalysis.possible_fixes.map((fix, i) => (
                    <li key={i}>{fix}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
