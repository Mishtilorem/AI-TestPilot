from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project

project_repo = ProjectRepository()


class ProjectService:
    def get_owned(self, db: Session, project_id: str, user_id: str) -> Project:
        """Fetch a project and enforce that it belongs to the requesting user."""
        project = project_repo.get(db, project_id)
        if not project or project.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    def list_for_user(self, db: Session, user_id: str, skip: int = 0, limit: int = 50) -> list[Project]:
        return project_repo.get_by_user(db, user_id, skip=skip, limit=limit)

    def create(self, db: Session, user_id: str, data: ProjectCreate) -> Project:
        project = Project(
            user_id=user_id,
            name=data.name,
            description=data.description,
            target_url=str(data.target_url),
        )
        return project_repo.create(db, project)

    def update(self, db: Session, project_id: str, user_id: str, data: ProjectUpdate) -> Project:
        project = self.get_owned(db, project_id, user_id)
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.target_url is not None:
            project.target_url = str(data.target_url)
        return project_repo.update(db, project)

    def delete(self, db: Session, project_id: str, user_id: str) -> None:
        project = self.get_owned(db, project_id, user_id)
        project_repo.delete(db, project)


project_service = ProjectService()
