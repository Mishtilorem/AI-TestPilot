"use client";

import Link from "next/link";
import { ArrowLeft, ExternalLink } from "lucide-react";
import { useProject } from "@/hooks/use-projects";
import { RequirementsTab } from "@/components/requirements/requirements-tab";
import { TestCasesTab } from "@/components/test-cases/test-cases-tab";
import { RunsTab } from "@/components/runs/runs-tab";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";

export default function ProjectDetailPage({ params }: { params: { id: string } }) {
  const { id } = params;
  const { data: project, isLoading } = useProject(id);

  if (isLoading) {
    return <Skeleton className="h-40 w-full" />;
  }

  if (!project) {
    return <p className="text-muted-foreground">Project not found.</p>;
  }

  return (
    <div className="space-y-6">
      <Link
        href="/projects"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" /> Back to projects
      </Link>

      <div>
        <h1 className="text-2xl font-bold">{project.name}</h1>
        <p className="text-sm text-muted-foreground">{project.description || "No description"}</p>
        <a
          href={project.target_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-1 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ExternalLink className="h-3 w-3" /> {project.target_url}
        </a>
      </div>

      <Tabs defaultValue="requirements">
        <TabsList>
          <TabsTrigger value="requirements">Requirements</TabsTrigger>
          <TabsTrigger value="test-cases">Test Cases</TabsTrigger>
          <TabsTrigger value="runs">Runs</TabsTrigger>
        </TabsList>
        <TabsContent value="requirements" className="mt-4">
          <RequirementsTab projectId={id} />
        </TabsContent>
        <TabsContent value="test-cases" className="mt-4">
          <TestCasesTab projectId={id} />
        </TabsContent>
        <TabsContent value="runs" className="mt-4">
          <RunsTab projectId={id} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
