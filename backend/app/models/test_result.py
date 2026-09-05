from datetime import datetime
from sqlalchemy import String, Text, Enum, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import uuid
import enum


class ResultStatus(str, enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    test_run_id: Mapped[str] = mapped_column(
        String, ForeignKey("test_runs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    test_case_id: Mapped[str] = mapped_column(
        String, ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[ResultStatus] = mapped_column(Enum(ResultStatus), nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    screenshot_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    logs: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    run: Mapped["TestRun"] = relationship("TestRun", back_populates="results")
    test_case: Mapped["TestCase"] = relationship("TestCase", back_populates="results")
