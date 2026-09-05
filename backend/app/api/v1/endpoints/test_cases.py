from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate, TestCaseResponse
from app.schemas.common import MessageResponse
from app.services.test_case_service import test_case_service
from app.models.user import User

router = APIRouter(tags=["test-cases"])


@router.get("/projects/{project_id}/test-cases", response_model=list[TestCaseResponse])
def list_test_cases(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return test_case_service.list_for_project(db, project_id, current_user.id)


@router.post(
    "/projects/{project_id}/test-cases",
    response_model=TestCaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test_case(
    project_id: str,
    data: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return test_case_service.create(db, project_id, current_user.id, data)


@router.get("/test-cases/{test_case_id}", response_model=TestCaseResponse)
def get_test_case(
    test_case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return test_case_service.get_owned(db, test_case_id, current_user.id)


@router.patch("/test-cases/{test_case_id}", response_model=TestCaseResponse)
def update_test_case(
    test_case_id: str,
    data: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return test_case_service.update(db, test_case_id, current_user.id, data)


@router.delete("/test-cases/{test_case_id}", response_model=MessageResponse)
def delete_test_case(
    test_case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    test_case_service.delete(db, test_case_id, current_user.id)
    return MessageResponse(message="Test case deleted")
