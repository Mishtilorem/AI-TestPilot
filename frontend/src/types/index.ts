// Shapes mirror the FastAPI response models.

export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Project {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  target_url: string;
  created_at: string;
}

export interface Requirement {
  id: string;
  project_id: string;
  content: string;
  created_at: string;
}

export interface TestCase {
  id: string;
  project_id: string;
  requirement_id: string | null;
  title: string;
  description: string;
  expected_result: string;
  selenium_script: string | null;
  generated_by_ai: boolean;
  created_at: string;
}

export type RunStatus = "pending" | "running" | "completed" | "failed";
export type ResultStatus = "passed" | "failed" | "skipped" | "error";

export interface TestRun {
  id: string;
  project_id: string;
  status: RunStatus;
  browser: string;
  start_time: string | null;
  end_time: string | null;
  created_at: string;
}

export interface TestResult {
  id: string;
  test_run_id: string;
  test_case_id: string;
  status: ResultStatus;
  duration_seconds: number | null;
  screenshot_url: string | null;
  logs: string | null;
  ai_analysis: string | null;
  ai_confidence: number | null;
  created_at: string;
}

export interface TestRunDetail extends TestRun {
  results: TestResult[];
}
