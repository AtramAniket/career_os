from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

class ApplicationEvent(db.Model):

	__tablename__ = "application_events"

	id: Mapped[int] = mapped_column(primary_key=True)

	job_application_id: Mapped[int] = mapped_column(
		ForeignKey("job_applications.id", ondelete="CASCADE"),
		nullable=False,
		index=True)

	event_type: Mapped[str] = mapped_column(
		String(80),
		nullable=False)

	title: Mapped[str] = mapped_column(
		String(150),
		nullable=False)

	description: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True)

	event_date: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False)

	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		default=lambda: datetime.now(timezone.utc),
		nullable=False)

	job_application: Mapped["JobApplication"] = relationship(
		"JobApplication",
		back_populates="events")