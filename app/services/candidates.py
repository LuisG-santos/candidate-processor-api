from uuid import UUID

from app.repositories.candidates import CandidateRepository
from app.repositories.job import JobRepository


class CandidateService:
    def __init__(
        self, candidate_repository: CandidateRepository, job_repository: JobRepository
    ):
        self.candidate_repository = candidate_repository
        self.job_repository = job_repository

    def get_by_job_id(self, job_id: UUID):
        job = self.job_repository.get(job_id)

        if not job:
            raise ValueError("Job not found")

        candidates = self.candidate_repository.get_by_job_id(job_id)

        return candidates
