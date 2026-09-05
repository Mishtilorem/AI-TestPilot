from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.test_case import TestCase


class TestCaseRepository(BaseRepository[TestCase]):
    def __init__(self):
        super().__init__(TestCase)

    def get_by_project(self, db: Session, project_id: str) -> list[TestCase]:
        return (
            db.query(TestCase)
            .filter(TestCase.project_id == project_id)
            .order_by(TestCase.created_at.desc())
            .all()
        )

    def get_runnable_by_project(self, db: Session, project_id: str) -> list[TestCase]:
        """Test cases that have a generated Selenium script and can be executed."""
        return (
            db.query(TestCase)
            .filter(TestCase.project_id == project_id, TestCase.selenium_script.isnot(None))
            .all()
        )

    def count_by_project(self, db: Session, project_id: str) -> int:
        return db.query(TestCase).filter(TestCase.project_id == project_id).count()
