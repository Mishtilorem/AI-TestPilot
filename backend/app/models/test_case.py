from datetime import datetime
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import uuid


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(
        String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    requirement_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    expected_result: Mapped[str] = mapped_column(Text, nullable=False)
    selenium_script: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_by_ai: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped["Project"] = relationship("Project", back_populates="test_cases")
    requirement: Mapped["Requirement | None"] = relationship("Requirement", back_populates="test_cases")
    results: Mapped[list["TestResult"]] = relationship("TestResult", back_populates="test_case")
