from datetime import datetime
from pydantic import BaseModel, Field

class JobSchema(BaseModel):
    id: str
    filename: str
    status: str
    total_cadidates: int
    approved_candidates: int
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime
    