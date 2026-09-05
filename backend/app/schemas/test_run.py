from datetime import datetime
from pydantic import BaseModel
from app.models.test_run import RunStatus
from app.schemas.test_result import TestResultResponse


class TestRunCreate(BaseModel):
    browser: str = "chrome"


class TestRunResponse(BaseModel):
    id: str
    project_id: str
    status: RunStatus
    browser: str
    start_time: datetime | None
    end_time: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TestRunDetailResponse(TestRunResponse):
    results: list[TestResultResponse] = []
