from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.job import JobController
from app.database.session import get_session
from app.repositories.job import JobRepository
from app.services.job import JobService


def get_job_repository(session: Session = Depends(get_session)) -> JobRepository:  # noqa: B008
    return JobRepository(session)

def get_job_service(repository: JobRepository = Depends(get_job_repository)):  # noqa: B008
    return JobService(repository)

def get_job_controller(service: JobService = Depends(get_job_service)):  # noqa: B008
    return JobController(service)
