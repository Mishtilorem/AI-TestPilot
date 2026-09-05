from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.test_result import TestResult


class TestResultRepository(BaseRepository[TestResult]):
    def __init__(self):
        super().__init__(TestResult)

    def get_by_run(self, db: Session, run_id: str) -> list[TestResult]:
        return db.query(TestResult).filter(TestResult.test_run_id == run_id).all()
