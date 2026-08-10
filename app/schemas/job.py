from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.job import JobStatus


class JobCreate(BaseModel):
    filename: str


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    filename: str
    status: JobStatus
    total_candidates: int
    approved_candidates: int
    created_at: datetime
    completed_at: datetime | None
