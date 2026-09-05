from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.project import Project


class ProjectRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)

    def get_by_user(self, db: Session, user_id: str, skip: int = 0, limit: int = 50) -> list[Project]:
        return (
            db.query(Project)
            .filter(Project.user_id == user_id)
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_user(self, db: Session, user_id: str) -> int:
        return db.query(Project).filter(Project.user_id == user_id).count()
