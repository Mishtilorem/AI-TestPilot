"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { TestCase } from "@/types";

export function useTestCases(projectId: string) {
  return useQuery({
    queryKey: ["test-cases", projectId],
    queryFn: async () => {
      const { data } = await api.get<TestCase[]>(`/projects/${projectId}/test-cases`);
      return data;
    },
    enabled: !!projectId,
  });
}
