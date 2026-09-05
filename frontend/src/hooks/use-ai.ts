"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { TestCase, TestResult } from "@/types";

export function useGenerateTestCases(projectId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (requirementId: string) => {
      const { data } = await api.post<TestCase[]>(
        `/requirements/${requirementId}/generate-tests`
      );
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["test-cases", projectId] });
    },
  });
}

export function useGenerateScript(projectId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (testCaseId: string) => {
      const { data } = await api.post<TestCase>(
        `/test-cases/${testCaseId}/generate-script`
      );
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["test-cases", projectId] });
    },
  });
}

export function useAnalyzeFailure(runId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (resultId: string) => {
      const { data } = await api.post<TestResult>(`/results/${resultId}/analyze`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["run", runId] });
    },
  });
}
