"use client";

import { useState } from "react";
import { Sparkles, Loader2, Code2 } from "lucide-react";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { TestCase } from "@/types";
import { useTestCases } from "@/hooks/use-test-cases";
import { useGenerateScript } from "@/hooks/use-ai";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export function TestCasesTab({ projectId }: { projectId: string }) {
  const { data: testCases, isLoading } = useTestCases(projectId);
  const generateScript = useGenerateScript(projectId);
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  const [viewing, setViewing] = useState<TestCase | null>(null);

  async function onGenerate(id: string) {
    setGeneratingId(id);
    try {
      await generateScript.mutateAsync(id);
      toast.success("Selenium script generated");
    } catch (err) {
      const message =
        err instanceof AxiosError
          ? err.response?.data?.detail ?? "Generation failed"
          : "Generation failed";
      toast.error(message);
    } finally {
      setGeneratingId(null);
    }
  }

  if (isLoading) {
    return <Skeleton className="h-40 w-full" />;
  }

  if (!testCases || testCases.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        No test cases yet. Add a requirement and click &quot;Generate Test Cases&quot;.
      </p>
    );
  }

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Title</TableHead>
            <TableHead>Source</TableHead>
            <TableHead>Script</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {testCases.map((tc) => {
            const busy = generatingId === tc.id;
            return (
              <TableRow key={tc.id}>
                <TableCell className="font-medium">{tc.title}</TableCell>
                <TableCell>
                  <Badge variant={tc.generated_by_ai ? "default" : "secondary"}>
                    {tc.generated_by_ai ? "AI" : "Manual"}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge variant={tc.selenium_script ? "default" : "outline"}>
                    {tc.selenium_script ? "Ready" : "None"}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    {tc.selenium_script && (
                      <Button variant="outline" size="sm" onClick={() => setViewing(tc)}>
                        <Code2 className="mr-2 h-4 w-4" />
                        View
                      </Button>
                    )}
                    <Button size="sm" onClick={() => onGenerate(tc.id)} disabled={busy}>
                      {busy ? (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      ) : (
                        <Sparkles className="mr-2 h-4 w-4" />
                      )}
                      {tc.selenium_script ? "Regenerate" : "Generate Script"}
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>

      <Dialog open={!!viewing} onOpenChange={(open) => !open && setViewing(null)}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>{viewing?.title}</DialogTitle>
          </DialogHeader>
          <pre className="max-h-[60vh] overflow-auto rounded-md bg-muted p-4 text-xs">
            <code>{viewing?.selenium_script}</code>
          </pre>
        </DialogContent>
      </Dialog>
    </>
  );
}
