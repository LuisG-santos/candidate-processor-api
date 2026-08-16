from uuid import UUID

from fastapi import HTTPException, status

from app.services.candidates import CandidateService


class CandidateController:
    def __init__(self, candidate_service: CandidateService):
        self.candidate_service = candidate_service

    def get_by_job_id(self, job_id: UUID):
        try:
            candidates = self.candidate_service.get_by_job_id(job_id)
            return candidates
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
            )
