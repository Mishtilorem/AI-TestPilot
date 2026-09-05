from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_projects: int
    total_test_cases: int
    total_runs: int
    pass_rate: float
