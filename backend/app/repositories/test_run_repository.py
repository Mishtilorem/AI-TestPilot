from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.test_run import TestRun


class TestRunRepository(BaseRepository[TestRun]):
    def __init__(self):
        super().__init__(TestRun)

    def get_by_project(self, db: Session, project_id: str, skip: int = 0, limit: int = 50) -> list[TestRun]:
        return (
            db.query(TestRun)
            .filter(TestRun.project_id == project_id)
            .order_by(TestRun.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_project(self, db: Session, project_id: str) -> int:
        return db.query(TestRun).filter(TestRun.project_id == project_id).count()
