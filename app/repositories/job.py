from uuid import UUID

from sqlalchemy.orm import Session

from app.models.job import JobModel


class JobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, job: JobModel) -> JobModel:
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)

        return job

    def get(self, job_id: UUID) -> JobModel | None:
        job = self.session.get(JobModel, job_id)

        return job
