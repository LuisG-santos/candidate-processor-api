from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    email: str
    phone: str
    note: int
    created_at: datetime
    
    
    
    
    