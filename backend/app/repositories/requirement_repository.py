from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.requirement import Requirement


class RequirementRepository(BaseRepository[Requirement]):
    def __init__(self):
        super().__init__(Requirement)

    def get_by_project(self, db: Session, project_id: str) -> list[Requirement]:
        return (
            db.query(Requirement)
            .filter(Requirement.project_id == project_id)
            .order_by(Requirement.created_at.desc())
            .all()
        )
