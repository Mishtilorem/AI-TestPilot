"use client";

import { FolderKanban, FileCheck2, PlayCircle, CheckCircle2 } from "lucide-react";
import { useDashboardStats } from "@/hooks/use-dashboard";
import { StatCard } from "@/components/dashboard/stat-card";
import { Skeleton } from "@/components/ui/skeleton";

export default function DashboardPage() {
  const { data: stats, isLoading } = useDashboardStats();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-sm text-muted-foreground">Overview of your testing activity</p>
      </div>

      {isLoading || !stats ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-28 w-full" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Total Projects" value={stats.total_projects} icon={FolderKanban} />
          <StatCard title="Test Cases" value={stats.total_test_cases} icon={FileCheck2} />
          <StatCard title="Test Runs" value={stats.total_runs} icon={PlayCircle} />
          <StatCard title="Pass Rate" value={`${stats.pass_rate}%`} icon={CheckCircle2} />
        </div>
      )}
    </div>
  );
}
