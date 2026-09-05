"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { TestRun, TestRunDetail } from "@/types";

export function useRuns(projectId: string) {
  return useQuery({
    queryKey: ["runs", projectId],
    queryFn: async () => {
      const { data } = await api.get<TestRun[]>(`/projects/${projectId}/runs`);
      return data;
    },
    enabled: !!projectId,
  });
}

export function useRun(runId: string) {
  return useQuery({
    queryKey: ["run", runId],
    queryFn: async () => {
      const { data } = await api.get<TestRunDetail>(`/runs/${runId}`);
      return data;
    },
    enabled: !!runId,
  });
}

export function useStartRun(projectId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data } = await api.post<TestRun>(`/projects/${projectId}/runs`, {
        browser: "chrome",
      });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["runs", projectId] });
    },
  });
}
