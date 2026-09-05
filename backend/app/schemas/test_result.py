from datetime import datetime
from pydantic import BaseModel
from app.models.test_result import ResultStatus


class TestResultResponse(BaseModel):
    id: str
    test_run_id: str
    test_case_id: str
    status: ResultStatus
    duration_seconds: float | None
    screenshot_url: str | None
    logs: str | None
    ai_analysis: str | None
    ai_confidence: float | None
    created_at: datetime

    model_config = {"from_attributes": True}
