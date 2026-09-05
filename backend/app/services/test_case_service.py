from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.test_case_repository import TestCaseRepository
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate
from app.models.test_case import TestCase
from app.services.project_service import project_service

test_case_repo = TestCaseRepository()


class TestCaseService:
    def get_owned(self, db: Session, test_case_id: str, user_id: str) -> TestCase:
        test_case = test_case_repo.get(db, test_case_id)
        if not test_case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test case not found")
        project_service.get_owned(db, test_case.project_id, user_id)
        return test_case

    def list_for_project(self, db: Session, project_id: str, user_id: str) -> list[TestCase]:
        project_service.get_owned(db, project_id, user_id)
        return test_case_repo.get_by_project(db, project_id)

    def create(self, db: Session, project_id: str, user_id: str, data: TestCaseCreate) -> TestCase:
        project_service.get_owned(db, project_id, user_id)
        test_case = TestCase(
            project_id=project_id,
            requirement_id=data.requirement_id,
            title=data.title,
            description=data.description,
            expected_result=data.expected_result,
            generated_by_ai=data.generated_by_ai,
        )
        return test_case_repo.create(db, test_case)

    def update(self, db: Session, test_case_id: str, user_id: str, data: TestCaseUpdate) -> TestCase:
        test_case = self.get_owned(db, test_case_id, user_id)
        if data.title is not None:
            test_case.title = data.title
        if data.description is not None:
            test_case.description = data.description
        if data.expected_result is not None:
            test_case.expected_result = data.expected_result
        if data.selenium_script is not None:
            test_case.selenium_script = data.selenium_script
        return test_case_repo.update(db, test_case)

    def delete(self, db: Session, test_case_id: str, user_id: str) -> None:
        test_case = self.get_owned(db, test_case_id, user_id)
        test_case_repo.delete(db, test_case)


test_case_service = TestCaseService()
