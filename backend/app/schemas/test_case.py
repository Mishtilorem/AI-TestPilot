from datetime import datetime
from pydantic import BaseModel, Field


class TestCaseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1)
    expected_result: str = Field(min_length=1)
    requirement_id: str | None = None
    generated_by_ai: bool = False


class TestCaseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    expected_result: str | None = None
    selenium_script: str | None = None


class TestCaseResponse(BaseModel):
    id: str
    project_id: str
    requirement_id: str | None
    title: str
    description: str
    expected_result: str
    selenium_script: str | None
    generated_by_ai: bool
    created_at: datetime

    model_config = {"from_attributes": True}
