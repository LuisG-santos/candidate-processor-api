from app.models.job import JobModel
from app.repositories.job import JobRepository
from app.schemas.job import JobCreate


class JobService:
    def __init__(self, jobRepository: JobRepository):
        self.repository = jobRepository

    def create_job(self, data: JobCreate):
        job = JobModel(filename=data.filename)

        return self.repository.create(job)
