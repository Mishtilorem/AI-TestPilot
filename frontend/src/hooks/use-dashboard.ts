"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface DashboardStats {
  total_projects: number;
  total_test_cases: number;
  total_runs: number;
  pass_rate: number;
}

export function useDashboardStats() {
  return useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: async () => {
      const { data } = await api.get<DashboardStats>("/dashboard/stats");
      return data;
    },
  });
}
