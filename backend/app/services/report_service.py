from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.test_case import TestCase
from app.models.test_run import TestRun
from app.models.test_result import TestResult, ResultStatus


class ReportService:
    def dashboard_stats(self, db: Session, user_id: str) -> dict:
        """Aggregate headline numbers across all of the user's projects."""
        total_projects = (
            db.query(func.count(Project.id)).filter(Project.user_id == user_id).scalar() or 0
        )

        total_test_cases = (
            db.query(func.count(TestCase.id))
            .join(Project, TestCase.project_id == Project.id)
            .filter(Project.user_id == user_id)
            .scalar()
            or 0
        )

        total_runs = (
            db.query(func.count(TestRun.id))
            .join(Project, TestRun.project_id == Project.id)
            .filter(Project.user_id == user_id)
            .scalar()
            or 0
        )

        # Pass rate across every stored test result belonging to the user.
        results_q = (
            db.query(TestResult.status)
            .join(TestRun, TestResult.test_run_id == TestRun.id)
            .join(Project, TestRun.project_id == Project.id)
            .filter(Project.user_id == user_id)
        )
        total_results = results_q.count()
        passed = results_q.filter(TestResult.status == ResultStatus.PASSED).count()
        pass_rate = round(passed / total_results * 100, 1) if total_results else 0.0

        return {
            "total_projects": total_projects,
            "total_test_cases": total_test_cases,
            "total_runs": total_runs,
            "pass_rate": pass_rate,
        }


report_service = ReportService()
