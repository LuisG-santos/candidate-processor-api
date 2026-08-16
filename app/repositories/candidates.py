from uuid import UUID

from sqlalchemy import select

from app.database.session import Session
from app.models.candidates import CandidatesModel


class CandidateRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_job_id(self, job_id: UUID) -> list[CandidatesModel]:
        stmt = select(CandidatesModel).where(CandidatesModel.job_id == job_id)
        result = self.session.execute(stmt)
        candidates = result.scalars().all()
        
        return candidates
        
        
        