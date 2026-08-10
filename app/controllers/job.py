from uuid import UUID

from fastapi import HTTPException, status

from app.schemas.job import JobCreate, JobCreateResponse
from app.services.job import JobService


class JobController:
    def __init__(self, job_service: JobService):
        self.service = job_service

    def create_job(self, data: JobCreate) -> JobCreateResponse:
        try:
            new_job = self.service.create_job(data)
            return new_job
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            )

    def get_job(self, job_id: UUID):
        try:
            job = self.service.get_job(job_id)
            return job
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
            )
