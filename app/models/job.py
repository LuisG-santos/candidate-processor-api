import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class JobStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobModel(Base):
    __tablename__ = "job"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column()
    total_candidates: Mapped[int] = mapped_column(default=0)
    approved_candidates: Mapped[int] = mapped_column(default=0)
    status: Mapped[JobStatus] = mapped_column(
        SQLEnum(JobStatus), default=JobStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    completed_at: Mapped[datetime | None] = mapped_column(default=None)
