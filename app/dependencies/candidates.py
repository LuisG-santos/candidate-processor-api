from fastapi import Depends

from app.controllers.candidates import CandidateController
from app.database.session import Session, get_session
from app.repositories.candidates import CandidateRepository
from app.repositories.job import JobRepository
from app.services.candidates import CandidateService


def get_candidates_repository(
    session: Session = Depends(get_session),  # noqa: B008
) -> CandidateRepository:
    return CandidateRepository(session)


def get_job_repository(session: Session = Depends(get_session)) -> JobRepository:  # noqa: B008
    return JobRepository(session)


def get_candidates_service(
    candidates_repository: CandidateRepository = Depends(get_candidates_repository),  # noqa: B008
    job_repository: JobRepository = Depends(get_job_repository),  # noqa: B008
) -> CandidateService:
    return CandidateService(candidates_repository, job_repository)


def get_candidates_controller(
    candidates_service: CandidateService = Depends(get_candidates_service),  # noqa: B008
) -> CandidateController:
    return CandidateController(candidates_service)
