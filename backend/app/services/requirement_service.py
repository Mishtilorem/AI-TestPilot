from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.requirement_repository import RequirementRepository
from app.schemas.requirement import RequirementCreate, RequirementUpdate
from app.models.requirement import Requirement
from app.services.project_service import project_service

requirement_repo = RequirementRepository()


class RequirementService:
    def get_owned(self, db: Session, requirement_id: str, user_id: str) -> Requirement:
        requirement = requirement_repo.get(db, requirement_id)
        if not requirement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found")
        # Enforce ownership via the parent project.
        project_service.get_owned(db, requirement.project_id, user_id)
        return requirement

    def list_for_project(self, db: Session, project_id: str, user_id: str) -> list[Requirement]:
        project_service.get_owned(db, project_id, user_id)
        return requirement_repo.get_by_project(db, project_id)

    def create(self, db: Session, project_id: str, user_id: str, data: RequirementCreate) -> Requirement:
        project_service.get_owned(db, project_id, user_id)
        requirement = Requirement(project_id=project_id, content=data.content)
        return requirement_repo.create(db, requirement)

    def update(self, db: Session, requirement_id: str, user_id: str, data: RequirementUpdate) -> Requirement:
        requirement = self.get_owned(db, requirement_id, user_id)
        if data.content is not None:
            requirement.content = data.content
        return requirement_repo.update(db, requirement)

    def delete(self, db: Session, requirement_id: str, user_id: str) -> None:
        requirement = self.get_owned(db, requirement_id, user_id)
        requirement_repo.delete(db, requirement)


requirement_service = RequirementService()
