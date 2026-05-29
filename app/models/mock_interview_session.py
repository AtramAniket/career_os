from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

class MockInterviewSession(db.Model):

	__tablename__ = "mock_interview_sessions"

	id: Mapped[int] = mapped_column(
		Integer,
		primary_key=True
	)

	user_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	job_application_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("job_applications.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	title: Mapped[Optional[str]] = mapped_column(
		String(150),
		nullable=True
	)

	status: Mapped[str] = mapped_column(
		String(20),
		nullable=False,
		default="server"
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False
	)

	completed_at: Mapped[Optional[datetime]] = mapped_column(
		DateTime(timezone=True),
		nullable=True
	)

	user: Mapped["User"] = relationship(
		"User",
		back_populates="mock_interview_sessions"
	)

	job_application: Mapped["JobApplication"] = relationship(
		"JobApplication",
		back_populates="mock_interview_sessions"
	)

	mock_interview_questions: Mapped["MockInterviewQuestion"] = relationship(
		"MockInterviewQuestion",
		back_populates="mock_interview_sessions"
	)