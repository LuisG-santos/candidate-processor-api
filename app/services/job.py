from uuid import UUID

from app.aws.s3 import generate_upload_url
from app.config.settings import settings
from app.models.job import JobModel
from app.repositories.job import JobRepository
from app.schemas.job import JobCreate, JobCreateResponse


class JobService:
    def __init__(self, jobRepository: JobRepository):
        self.repository = jobRepository

    def create_job(self, data: JobCreate):
        job = JobModel(filename=data.filename)
        job = self.repository.create(job)
        key = f"jobs/{job.id}/input/{job.filename}"
        url = generate_upload_url(str(settings.bucket_name), key)
    
        response = JobCreateResponse(
            id=job.id, 
            filename=job.filename, 
            upload_url=url
            )
    
        return response

    def get_job(self, job_id: UUID):
        job = self.repository.get(job_id)

        if job is None:
            raise ValueError("Job not found")
        return job
