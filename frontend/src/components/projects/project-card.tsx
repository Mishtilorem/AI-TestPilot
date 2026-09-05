"use client";

import Link from "next/link";
import { Trash2, ExternalLink } from "lucide-react";
import { AxiosError } from "axios";
import { toast } from "sonner";
import { Project } from "@/types";
import { useDeleteProject } from "@/hooks/use-projects";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function ProjectCard({ project }: { project: Project }) {
  const deleteProject = useDeleteProject();

  async function onDelete(e: React.MouseEvent) {
    e.preventDefault();
    if (!confirm(`Delete project "${project.name}"?`)) return;
    try {
      await deleteProject.mutateAsync(project.id);
      toast.success("Project deleted");
    } catch (err) {
      const message =
        err instanceof AxiosError
          ? err.response?.data?.detail ?? "Failed to delete"
          : "Failed to delete";
      toast.error(message);
    }
  }

  return (
    <Link href={`/projects/${project.id}`}>
      <Card className="h-full transition-colors hover:border-primary">
        <CardHeader className="flex flex-row items-start justify-between space-y-0">
          <CardTitle className="text-lg">{project.name}</CardTitle>
          <Button
            variant="ghost"
            size="icon"
            onClick={onDelete}
            disabled={deleteProject.isPending}
            aria-label="Delete project"
          >
            <Trash2 className="h-4 w-4 text-muted-foreground" />
          </Button>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="line-clamp-2 text-sm text-muted-foreground">
            {project.description || "No description"}
          </p>
          <p className="flex items-center gap-1 text-xs text-muted-foreground">
            <ExternalLink className="h-3 w-3" />
            {project.target_url}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}
