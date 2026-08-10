from fastapi import APIRouter, Depends, status

from app.controllers.job import JobController
from app.dependencies.job import get_job_controller
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/job")

@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(data: JobCreate, controller: JobController = Depends(get_job_controller)):  # noqa: B008
    return controller.create_job(data)
