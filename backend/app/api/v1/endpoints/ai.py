from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.test_case import TestCaseResponse
from app.schemas.test_result import TestResultResponse
from app.services.ai_service import ai_service
from app.services.requirement_service import requirement_service
from app.services.test_case_service import test_case_service
from app.services.project_service import project_service
from app.services.test_runner_service import test_runner_service
from app.repositories.test_result_repository import TestResultRepository
from app.repositories.test_case_repository import TestCaseRepository
from app.models.user import User

router = APIRouter(tags=["ai"])
result_repo = TestResultRepository()
tc_repo = TestCaseRepository()


@router.post(
    "/requirements/{requirement_id}/generate-tests",
    response_model=list[TestCaseResponse],
)
async def generate_test_cases(
    requirement_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requirement = requirement_service.get_owned(db, requirement_id, current_user.id)
    project = project_service.get_owned(db, requirement.project_id, current_user.id)
    return await ai_service.generate_test_cases(
        db,
        project_id=project.id,
        requirement_id=requirement.id,
        requirement_content=requirement.content,
        target_url=project.target_url,
    )


@router.post(
    "/test-cases/{test_case_id}/generate-script",
    response_model=TestCaseResponse,
)
async def generate_selenium_script(
    test_case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    test_case = test_case_service.get_owned(db, test_case_id, current_user.id)
    project = project_service.get_owned(db, test_case.project_id, current_user.id)
    return await ai_service.generate_selenium_script(db, test_case, project.target_url)


@router.post("/results/{result_id}/analyze", response_model=TestResultResponse)
async def analyze_failure(
    result_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = result_repo.get(db, result_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")
    # Ownership: result -> run -> project -> user.
    test_runner_service.get_owned_run(db, result.test_run_id, current_user.id)
    test_case = tc_repo.get(db, result.test_case_id)
    if not test_case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")
    return await ai_service.analyze_failure(db, result, test_case)
