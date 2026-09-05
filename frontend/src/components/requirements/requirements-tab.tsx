"use client";

import { useState } from "react";
import { Trash2, Sparkles, Loader2 } from "lucide-react";
import { AxiosError } from "axios";
import { toast } from "sonner";
import {
  useRequirements,
  useCreateRequirement,
  useDeleteRequirement,
} from "@/hooks/use-requirements";
import { useGenerateTestCases } from "@/hooks/use-ai";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof AxiosError
    ? err.response?.data?.detail ?? fallback
    : fallback;
}

export function RequirementsTab({ projectId }: { projectId: string }) {
  const { data: requirements, isLoading } = useRequirements(projectId);
  const createRequirement = useCreateRequirement(projectId);
  const deleteRequirement = useDeleteRequirement(projectId);
  const generateTestCases = useGenerateTestCases(projectId);
  const [content, setContent] = useState("");
  const [generatingId, setGeneratingId] = useState<string | null>(null);

  async function onAdd() {
    if (!content.trim()) return;
    try {
      await createRequirement.mutateAsync(content.trim());
      setContent("");
      toast.success("Requirement added");
    } catch (err) {
      toast.error(errorMessage(err, "Failed to add"));
    }
  }

  async function onGenerate(requirementId: string) {
    setGeneratingId(requirementId);
    try {
      const cases = await generateTestCases.mutateAsync(requirementId);
      toast.success(`Generated ${cases.length} test cases — see the Test Cases tab`);
    } catch (err) {
      toast.error(errorMessage(err, "Generation failed"));
    } finally {
      setGeneratingId(null);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <Input
          placeholder="User should be able to login using email and password."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onAdd()}
        />
        <Button onClick={onAdd} disabled={createRequirement.isPending}>
          Add
        </Button>
      </div>

      {isLoading ? (
        <Skeleton className="h-24 w-full" />
      ) : requirements && requirements.length > 0 ? (
        <div className="space-y-2">
          {requirements.map((r) => {
            const busy = generatingId === r.id;
            return (
              <Card key={r.id}>
                <CardContent className="flex items-center justify-between gap-2 py-3">
                  <p className="text-sm">{r.content}</p>
                  <div className="flex shrink-0 items-center gap-1">
                    <Button size="sm" onClick={() => onGenerate(r.id)} disabled={busy}>
                      {busy ? (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      ) : (
                        <Sparkles className="mr-2 h-4 w-4" />
                      )}
                      {busy ? "Generating..." : "Generate Test Cases"}
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => deleteRequirement.mutate(r.id)}
                      aria-label="Delete requirement"
                    >
                      <Trash2 className="h-4 w-4 text-muted-foreground" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">No requirements yet.</p>
      )}
    </div>
  );
}
