"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { Requirement } from "@/types";

export function useRequirements(projectId: string) {
  return useQuery({
    queryKey: ["requirements", projectId],
    queryFn: async () => {
      const { data } = await api.get<Requirement[]>(`/projects/${projectId}/requirements`);
      return data;
    },
    enabled: !!projectId,
  });
}

export function useCreateRequirement(projectId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (content: string) => {
      const { data } = await api.post<Requirement>(
        `/projects/${projectId}/requirements`,
        { content }
      );
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["requirements", projectId] });
    },
  });
}

export function useDeleteRequirement(projectId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/requirements/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["requirements", projectId] });
    },
  });
}
