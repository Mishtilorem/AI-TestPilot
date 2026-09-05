from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.test_run_repository import TestRunRepository
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_case_repository import TestCaseRepository
from app.services.project_service import project_service
from app.selenium.runner import execute_script
from app.models.test_run import TestRun, RunStatus
from app.models.test_result import TestResult

run_repo = TestRunRepository()
result_repo = TestResultRepository()
test_case_repo = TestCaseRepository()


class TestRunnerService:
    def get_owned_run(self, db: Session, run_id: str, user_id: str) -> TestRun:
        run = run_repo.get(db, run_id)
        if not run:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
        project_service.get_owned(db, run.project_id, user_id)
        return run

    def list_for_project(self, db: Session, project_id: str, user_id: str) -> list[TestRun]:
        project_service.get_owned(db, project_id, user_id)
        return run_repo.get_by_project(db, project_id)

    def start_run(self, db: Session, project_id: str, user_id: str, browser: str = "chrome") -> TestRun:
        """Create a run, execute every test case that has a script, store results.

        Runs synchronously: the request returns once all tests have finished.
        """
        project = project_service.get_owned(db, project_id, user_id)
        runnable = test_case_repo.get_runnable_by_project(db, project_id)
        if not runnable:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No test cases with generated scripts to run",
            )

        run = TestRun(
            project_id=project_id,
            browser=browser,
            status=RunStatus.RUNNING,
            start_time=datetime.now(timezone.utc),
        )
        run = run_repo.create(db, run)

        for test_case in runnable:
            outcome = execute_script(
                test_case.selenium_script,
                project.target_url,
                run_id=run.id,
                test_case_id=test_case.id,
            )
            result = TestResult(
                test_run_id=run.id,
                test_case_id=test_case.id,
                status=outcome["status"],
                duration_seconds=outcome["duration_seconds"],
                logs=outcome["logs"],
                screenshot_url=outcome["screenshot_url"],
            )
            result_repo.create(db, result)

        run.status = RunStatus.COMPLETED
        run.end_time = datetime.now(timezone.utc)
        return run_repo.update(db, run)


test_runner_service = TestRunnerService()
