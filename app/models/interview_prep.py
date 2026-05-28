from typing import Optional
from datetime import datetime, timezone

from app.extensions import db

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, JSON, Boolean

class InterviewPrep(db.Model):

	__tablename__ = "interview_preps"

	id: Mapped[int] = mapped_column(
		Integer,
		primary_key=True
	)

	job_application_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("job_applications.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	resume_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("application_documents.id", ondelete="SET NULL"),
		nullable=True
	)

	prep_type: Mapped[str] = mapped_column(
		String(50),
		nullable=False,
		default="general"
	)

	strategy_summary: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True
	)

	questions_json: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	is_latest: Mapped[bool] = mapped_column(
		Boolean,
		default=True,
		nullable=False
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		default=lambda : datetime.now(timezone.utc)
	)

	job_application: Mapped["JobApplication"] = relationship(
		"JobApplication",
		back_populates="interview_preps")

	source_resume: Mapped["ApplicationDocument"] = relationship(
		"ApplicationDocument",
		back_populates="interview_preps")