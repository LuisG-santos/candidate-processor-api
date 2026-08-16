from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.controllers.candidates import CandidateController
from app.controllers.job import JobController
from app.dependencies.candidates import get_candidates_controller
from app.dependencies.job import get_job_controller
from app.schemas.candidates import CandidateResponse
from app.schemas.job import JobCreate, JobCreateResponse, JobResponse

router = APIRouter(prefix="/job")


@router.post("", response_model=JobCreateResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    data: JobCreate,
    controller: JobController = Depends(get_job_controller),  # noqa: B008
):
    return controller.create_job(data)


@router.get("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
def get_job(
    job_id: UUID, 
    controller: JobController = Depends(get_job_controller),  # noqa: B008
    ):  
    return controller.get_job(job_id)


@router.get(
    "/{job_id}/candidates",
    response_model=list[CandidateResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_job_id(
    job_id: UUID,
    controller: CandidateController = Depends(get_candidates_controller),  # noqa: B008
):
    return controller.get_by_job_id(job_id)