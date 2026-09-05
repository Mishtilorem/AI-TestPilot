from datetime import datetime
from pydantic import BaseModel, Field


class RequirementCreate(BaseModel):
    content: str = Field(min_length=1)


class RequirementUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1)


class RequirementResponse(BaseModel):
    id: str
    project_id: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
