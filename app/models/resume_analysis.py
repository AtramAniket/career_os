from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, Integer, Text, JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

class ResumeAnalysis(db.Model):

	__tablename__ = "resume_analyses"

	id: Mapped[int] = mapped_column(
		primary_key=True
	)

	job_application_id: Mapped[int] = mapped_column(
		ForeignKey("job_applications.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	document_id: Mapped[int] = mapped_column(
		ForeignKey("application_documents.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	ats_score: Mapped[Optional[int]] = mapped_column(
		Integer,
		nullable=True
	)

	ats_observations: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	keyword_match_score: Mapped[Optional[int]] = mapped_column(
		Integer,
		nullable=True
	)

	analysis_summary: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True
	)

	strengths: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	weakness: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	missing_keywords: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	suggestions: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	is_latest: Mapped[bool] = mapped_column(
		Boolean,
		default=True,
		nullable=False,
		server_default=db.true()
	)

	analysis_type: Mapped[str] = mapped_column(
		String(50),
		nullable=False,
		default="resume_review",
		server_default="resume_review"
	)

	improved_summary: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True
	)

	bullet_improvements: Mapped[Optional[list]] = mapped_column(
		JSON,
		nullable=True
	)

	recruiter_impression: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		onupdate=lambda: datetime.now(timezone.utc),
		nullable=False
	)

	application = relationship(
		"JobApplication",
		back_populates="resume_analyses"
	)

	document = relationship(
		"ApplicationDocument",
		back_populates="resume_analyses"
	)

