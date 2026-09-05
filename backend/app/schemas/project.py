from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    target_url: HttpUrl


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    target_url: HttpUrl | None = None


class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str | None
    target_url: str
    created_at: datetime

    model_config = {"from_attributes": True}
