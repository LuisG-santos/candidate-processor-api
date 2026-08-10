from fastapi import HTTPException, status

from app.models.job import JobModel
from app.schemas.job import JobCreate
from app.services.job import JobService


class JobController:
    def __init__(self, job_service: JobService):
        self.service = job_service

    def create_job(self, data: JobCreate) -> JobModel:
        try:
            new_job = self.service.create_job(data)
            return new_job
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            )
