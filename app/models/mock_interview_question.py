from typing import Optional
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, Integer, String, DateTime

from app.extensions import db

class MockInterviewQuestion(db.Model):

	__tablename__ = "mock_interview_questions"

	id: Mapped[id] = mapped_column(
		Integer,
		primary_key=True
	)

	session_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("mock_interview_sessions.id", ondelete="CASCADE"),
		index=True,
		nullable=False
	)

	question: Mapped[str] = mapped_column(
		Text,
		nullable=True
	)

	category: Mapped[str] = mapped_column(
		String(50),
		nullable=False,
		default="resume"
	)

	display_order: Mapped[int] = mapped_column(
		Integer,
		nullable=True
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False
	)
