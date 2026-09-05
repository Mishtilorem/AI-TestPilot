from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.test_run import TestRunCreate, TestRunResponse, TestRunDetailResponse
from app.services.test_runner_service import test_runner_service
from app.repositories.test_result_repository import TestResultRepository
from app.models.user import User

router = APIRouter(tags=["test-runs"])
result_repo = TestResultRepository()


@router.post(
    "/projects/{project_id}/runs",
    response_model=TestRunResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_run(
    project_id: str,
    data: TestRunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return test_runner_service.start_run(db, project_id, current_user.id, data.browser)


@router.get("/projects/{project_id}/runs", response_model=list[TestRunResponse])
def list_runs(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return test_runner_service.list_for_project(db, project_id, current_user.id)


@router.get("/runs/{run_id}", response_model=TestRunDetailResponse)
def get_run(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run = test_runner_service.get_owned_run(db, run_id, current_user.id)
    # Attach results for the detail view.
    run.results = result_repo.get_by_run(db, run_id)
    return run


@router.get("/runs/{run_id}/results")
def get_run_results(
    run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    test_runner_service.get_owned_run(db, run_id, current_user.id)
    return result_repo.get_by_run(db, run_id)
