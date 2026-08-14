import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CandidatesModel(Base):
    __tablename__ = "candidates"
    __table_args__ = (UniqueConstraint("job_id", "email"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, server_default=text("get_random_uuid()"))
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.id"), nullable=False)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    note: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, server_default=text("CURRENT_TIMESTAMP"))
