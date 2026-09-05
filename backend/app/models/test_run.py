from datetime import datetime
from sqlalchemy import String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import uuid
import enum


class RunStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TestRun(Base):
    __tablename__ = "test_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(
        String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.PENDING)
    browser: Mapped[str] = mapped_column(String(50), default="chrome")
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped["Project"] = relationship("Project", back_populates="test_runs")
    results: Mapped[list["TestResult"]] = relationship(
        "TestResult", back_populates="run", cascade="all, delete-orphan"
    )
