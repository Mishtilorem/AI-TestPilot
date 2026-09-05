from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.requirement import RequirementCreate, RequirementUpdate, RequirementResponse
from app.schemas.common import MessageResponse
from app.services.requirement_service import requirement_service
from app.models.user import User

router = APIRouter(tags=["requirements"])


@router.get("/projects/{project_id}/requirements", response_model=list[RequirementResponse])
def list_requirements(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return requirement_service.list_for_project(db, project_id, current_user.id)


@router.post(
    "/projects/{project_id}/requirements",
    response_model=RequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_requirement(
    project_id: str,
    data: RequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return requirement_service.create(db, project_id, current_user.id, data)


@router.patch("/requirements/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
    requirement_id: str,
    data: RequirementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return requirement_service.update(db, requirement_id, current_user.id, data)


@router.delete("/requirements/{requirement_id}", response_model=MessageResponse)
def delete_requirement(
    requirement_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requirement_service.delete(db, requirement_id, current_user.id)
    return MessageResponse(message="Requirement deleted")
